# Code in this file is copied and adapted from
# https://github.com/openai/evolution-strategies-starter and from
# https://github.com/modestyachts/ARS

from collections import namedtuple
import logging
import numpy as np
import time

import ray
from ray.rllib.agents import Trainer, with_common_config

from ray.rllib.agents.ars import optimizers
from ray.rllib.agents.ars import policies
from ray.rllib.agents.ars import utils
from ray.rllib.policy.sample_batch import DEFAULT_POLICY_ID
from ray.rllib.utils.annotations import override
from ray.rllib.utils.memory import ray_get_and_free
from ray.rllib.utils import FilterManager

from math import ceil

logger = logging.getLogger(__name__)

Result = namedtuple("Result", [
    "noise_indices", "noisy_returns", "sign_noisy_returns", "noisy_lengths",
    "eval_returns", "eval_lengths"
])

# yapf: disable
# __sphinx_doc_begin__
DEFAULT_CONFIG = with_common_config({
    "noise_stdev": 0.02,  # std deviation of parameter noise
    "num_rollouts": 32,  # number of perturbs to try
    "rollouts_used": 32,  # number of perturbs to keep in gradient estimate
    "num_workers": 2,
    "sgd_stepsize": 0.01,  # sgd step-size
    "observation_filter": "MeanStdFilter",
    "noise_size": 250000000,
    "eval_prob": 0.03,  # probability of evaluating the parameter rewards
    "report_length": 10,  # how many of the last rewards we average over
    "offset": 0,
})
# __sphinx_doc_end__
# yapf: enable


@ray.remote
def create_shared_noise(count):
    """Create a large array of noise to be shared by all workers."""
    seed = 123
    noise = np.random.RandomState(seed).randn(count).astype(np.float32)
    return noise



# e.g. configs = {"starting_leg_angle":{"min":[<min_val_ang1>,<min_val_ang2>], "max":[<max_val_ang1>,<max_val_ang2>]}}
@ray.remote
def create_random_env_configs(count, configs):
    """Create an array with random configurations for environments."""
    random_configs = []
    for key in configs.keys():
        num_params = len(configs[key]["min"])   # e.g. number of angles
        params = []
        for i in range(num_params):
            params.append(np.random.uniform(configs[key]["min"][i], configs[key]["max"][i],size=(count,)))
        
        for x in range(count):
            env_config = []
            for i in range(num_params):
                env_config.append(params[i][x])
            random_configs.append({key:np.array(env_config)})            

    return np.array(random_configs)

class SharedNoiseTable:
    def __init__(self, noise):
        self.noise = noise
        assert self.noise.dtype == np.float32

    def get(self, i, dim):
        return self.noise[i:i + dim]

    def sample_index(self, dim):
        return np.random.randint(0, len(self.noise) - dim + 1)

    def get_delta(self, dim):
        idx = self.sample_index(dim)
        return idx, self.get(idx, dim)

class SharedRandomEnvConfigsTable:
    def __init__(self, config):
        self.config = config

    def get(self, i=None):
        if(i is None):
            return self.config[int(np.random.uniform(0,self.len()-1))]

        return self.config[i]
        
    def len(self):
        return len(self.config)



@ray.remote
class Worker:
    def __init__(self, config, env_creator, noise, min_task_runtime=0.2):
        self.min_task_runtime = min_task_runtime
        self.config = config
        self.noise = SharedNoiseTable(noise)

        self.env = env_creator(config["env_config"])
        from ray.rllib import models
        self.preprocessor = models.ModelCatalog.get_preprocessor(self.env)

        self.sess = utils.make_session(single_threaded=True)
        self.policy = policies.GenericPolicy(
            self.sess, self.env.action_space, self.env.observation_space,
            self.preprocessor, config["observation_filter"], config["model"])


    def setRandomEnvConfig(self, random_env_configs):
        self.random_env_config = SharedRandomEnvConfigsTable(random_env_configs)

    @property
    def filters(self):
        return {DEFAULT_POLICY_ID: self.policy.get_filter()}

    def sync_filters(self, new_filters):
        for k in self.filters:
            self.filters[k].sync(new_filters[k])

    def get_filters(self, flush_after=False):
        return_filters = {}
        for k, f in self.filters.items():
            return_filters[k] = f.as_serializable()
            if flush_after:
                f.clear_buffer()
        return return_filters

    def rollout(self, timestep_limit, add_noise=False):
        rollout_rewards, rollout_length = policies.rollout(
            self.policy,
            self.env,
            timestep_limit=timestep_limit,
            add_noise=add_noise,
            offset=self.config["offset"])
        return rollout_rewards, rollout_length

    def do_rollouts(self, params, timestep_limit=None):
        # Set the network weights.
        self.policy.set_weights(params)

        noise_indices, returns, sign_returns, lengths = [], [], [], []
        eval_returns, eval_lengths = [], []

        # Perform some rollouts with noise.
        while (len(noise_indices) == 0):
            if np.random.uniform() < self.config["eval_prob"]:
                # Do an evaluation run with no perturbation.
                # Select the configurations for the environments randomly from the vector of radnom environment configurations
                # Set the new configuration for the environment
                randomized_env_config = self.random_env_config.get()    
                self.env.setConfig(randomized_env_config)
                self.policy.set_weights(params)
                rewards, length = self.rollout(timestep_limit, add_noise=False)
                eval_returns.append(rewards.sum())
                eval_lengths.append(length)
            else:
                # Do a regular run with parameter perturbations.
                noise_index = self.noise.sample_index(self.policy.num_params)

                perturbation = self.config["noise_stdev"] * self.noise.get(
                    noise_index, self.policy.num_params)


                # Select the configurations for the environments
                # Set the new configuration for the environment
                randomized_env_config = self.random_env_config.get(0)
                self.env.setConfig(randomized_env_config)

                self.policy.set_weights(params + perturbation)
                reward_pos, length_pos = self.rollout(timestep_limit)
                
                rewards_pos = reward_pos
                lengths_pos = length_pos

                self.policy.set_weights(params - perturbation)
                reward_neg, length_neg = self.rollout(timestep_limit)
                rewards_neg = reward_neg
                lengths_neg = length_neg

                # These two sampling steps could be done in parallel on
                # different actors letting us update twice as frequently.
                for i in range(1,self.random_env_config.len()):
                    # Select the configurations for the environments
                    # Set the new configuration for the environment
                    randomized_env_config = self.random_env_config.get(i)
                    self.env.setConfig(randomized_env_config)

                    self.policy.set_weights(params + perturbation)
                    reward_pos, length_pos = self.rollout(timestep_limit)
                    
                    rewards_pos = np.append(rewards_pos, reward_pos)
                    lengths_pos = np.append(lengths_pos, length_pos)

                    self.policy.set_weights(params - perturbation)
                    reward_neg, length_neg = self.rollout(timestep_limit)
                    rewards_neg = np.append(rewards_neg, reward_neg)
                    lengths_neg = np.append(lengths_neg, length_neg)


                returns.append([rewards_pos.sum()/self.random_env_config.len(), rewards_neg.sum()/self.random_env_config.len()])
                sign_returns.append(
                    [np.sign(rewards_pos).sum()/self.random_env_config.len(),
                    np.sign(rewards_neg).sum()/self.random_env_config.len()])
                lengths.append([lengths_pos.sum()/self.random_env_config.len(), lengths_neg.sum()/self.random_env_config.len()])

        return Result(
            noise_indices=noise_indices,
            noisy_returns=returns,
            sign_noisy_returns=sign_returns,
            noisy_lengths=lengths,
            eval_returns=eval_returns,
            eval_lengths=eval_lengths)


class ARSTrainer(Trainer):
    """Large-scale implementation of Augmented Random Search in Ray."""

    _name = "ARS"
    _default_config = DEFAULT_CONFIG

    @override(Trainer)
    def _init(self, config, env_creator):
        # PyTorch check.
        config["use_pytorch"] = False
        if config["use_pytorch"]:
            raise ValueError(
                "ARS does not support PyTorch yet! Use tf instead."
            )

        env = env_creator(config["env_config"])
        from ray.rllib import models
        preprocessor = models.ModelCatalog.get_preprocessor(env)

        self.sess = utils.make_session(single_threaded=False)
        self.policy = policies.GenericPolicy(
            self.sess, env.action_space, env.observation_space, preprocessor,
            config["observation_filter"], config["model"])
        self.optimizer = optimizers.SGD(self.policy, config["sgd_stepsize"])

        self.rollouts_used = config["rollouts_used"]
        self.num_rollouts = config["num_rollouts"]
        self.report_length = config["report_length"]

        # Create the shared noise table.
        logger.info("Creating shared noise table.")
        noise_id = create_shared_noise.remote(config["noise_size"])
        self.noise = SharedNoiseTable(ray.get(noise_id))

        self.extra_config = config["env_config"]["extra_trainer_configs"]
        self.domain_randomization_config = self.extra_config["domain_randomization"]
        
        
        self.domain_randomization_flag = False
        if(self.extra_config is not None):
            if("domain_randomization" in self.extra_config.keys()):
                domain_randomization = self.extra_config["domain_randomization"]
                self.domain_randomization_flag = True
                if("angle" in domain_randomization.keys()):
                    self.min_random_angles = [0,0]
                    self.max_random_angles = [0,0]
                    for i,flag in enumerate(domain_randomization["angle"][0]):
                        if(flag == True):
                            self.min_random_angles[i] = domain_randomization["angle"][1]
                            self.max_random_angles[i] = domain_randomization["angle"][2]

        # Create the actors.
        # TODO: Change Worker and add the config
        logger.info("Creating actors.")
        self.workers = [
            Worker.remote(config, env_creator, noise_id)
            for _ in range(config["num_workers"])
        ]


        self.episodes_so_far = 0
        self.reward_list = []
        self.tstart = time.time()

    @override(Trainer)
    def _train(self):
        config = self.config
        # Here the iteration starts
        # Create the random environments configurations for each iteration
        logger.info("Creating random environment configurations")


        # ceil(config["num_rollouts"]/config["num_workers"]*2)*config["num_workers"]
        #   is the exact number of environments created per iteration as the iteration is incremently
        #   increase by 2 (one for positive and one for negative perturbation) for each worker
        #   For each positive and negative perturbation, the same environment
        #   But if we do this it will be corrolated with number of rollouts and we will have less number of rollouts with different perturbations
        random_env_config_id = create_random_env_configs.remote(self.extra_config["num_randomized_envs"], self.domain_randomization_config)
        self.random_env_config = SharedRandomEnvConfigsTable(ray.get(random_env_config_id))
        for worker in self.workers:
            worker.setRandomEnvConfig.remote(random_env_config_id)

        theta = self.policy.get_weights()
        assert theta.dtype == np.float32

        # Put the current policy weights in the object store.
        theta_id = ray.put(theta)
        # Use the actors to do rollouts, note that we pass in the ID of the
        # policy weights.
        results, num_episodes, num_timesteps = self._collect_results(
            theta_id, config["num_rollouts"])

        all_noise_indices = []
        all_training_returns = []
        all_training_lengths = []
        all_eval_returns = []
        all_eval_lengths = []

        # Loop over the results.
        for result in results:
            all_eval_returns += result.eval_returns
            all_eval_lengths += result.eval_lengths

            all_noise_indices += result.noise_indices
            all_training_returns += result.noisy_returns
            all_training_lengths += result.noisy_lengths

        assert len(all_eval_returns) == len(all_eval_lengths)
        assert (len(all_noise_indices) == len(all_training_returns) ==
                len(all_training_lengths))

        self.episodes_so_far += num_episodes

        # Assemble the results.
        eval_returns = np.array(all_eval_returns)
        eval_lengths = np.array(all_eval_lengths)
        noise_indices = np.array(all_noise_indices)
        noisy_returns = np.array(all_training_returns)
        noisy_lengths = np.array(all_training_lengths)

        # keep only the best returns
        # select top performing directions if rollouts_used < num_rollouts
        max_rewards = np.max(noisy_returns, axis=1)
        if self.rollouts_used > self.num_rollouts:
            self.rollouts_used = self.num_rollouts

        percentile = 100 * (1 - (self.rollouts_used / self.num_rollouts))
        idx = np.arange(max_rewards.size)[
            max_rewards >= np.percentile(max_rewards, percentile)]
        noise_idx = noise_indices[idx]
        noisy_returns = noisy_returns[idx, :]

        # Compute and take a step.          It means take a step in changing the theta not take an action
        g, count = utils.batched_weighted_sum(
            noisy_returns[:, 0] - noisy_returns[:, 1],
            (self.noise.get(index, self.policy.num_params)
             for index in noise_idx),
            batch_size=min(500, noisy_returns[:, 0].size))
        g /= noise_idx.size
        # scale the returns by their standard deviation
        if not np.isclose(np.std(noisy_returns), 0.0):
            g /= np.std(noisy_returns)
        assert (g.shape == (self.policy.num_params, )
                and g.dtype == np.float32)
        # Compute the new weights theta.
        theta, update_ratio = self.optimizer.update(-g)
        # Set the new weights in the local copy of the policy.
        self.policy.set_weights(theta)
        # update the reward list
        if len(all_eval_returns) > 0:
            self.reward_list.append(eval_returns.mean())

        # Now sync the filters
        FilterManager.synchronize({
            DEFAULT_POLICY_ID: self.policy.get_filter()
        }, self.workers)

        info = {
            "weights_norm": np.square(theta).sum(),
            "weights_std": np.std(theta),
            "grad_norm": np.square(g).sum(),
            "update_ratio": update_ratio,
            "episodes_this_iter": noisy_lengths.size,
            "episodes_so_far": self.episodes_so_far,
        }
        result = dict(
            episode_reward_mean=np.mean(
                self.reward_list[-self.report_length:]),
            episode_len_mean=eval_lengths.mean(),
            timesteps_this_iter=noisy_lengths.sum(),
            info=info)

        return result

    @override(Trainer)
    def _stop(self):
        # workaround for https://github.com/ray-project/ray/issues/1516
        for w in self.workers:
            w.__ray_terminate__.remote()

    @override(Trainer)
    def compute_action(self, observation):
        return self.policy.compute(observation, update=True)[0]

    def _collect_results(self, theta_id, min_episodes):
        num_episodes, num_timesteps = 0, 0
        results = []
        while num_episodes < min_episodes:
            logger.debug(
                "Collected {} episodes {} timesteps so far this iter".format(
                    num_episodes, num_timesteps))
            rollout_ids = [
                worker.do_rollouts.remote(theta_id) for worker in self.workers
            ]
            # Get the results of the rollouts.
            for result in ray_get_and_free(rollout_ids):
                results.append(result)
                # Update the number of episodes and the number of timesteps
                # keeping in mind that result.noisy_lengths is a list of lists,
                # where the inner lists have length 2.
                num_episodes += sum(len(pair) for pair in result.noisy_lengths)
                num_timesteps += sum(
                    sum(pair) for pair in result.noisy_lengths)
        return results, num_episodes, num_timesteps

    def __getstate__(self):
        return {
            "weights": self.policy.get_weights(),
            "filter": self.policy.get_filter(),
            "episodes_so_far": self.episodes_so_far,
        }

    def __setstate__(self, state):
        self.episodes_so_far = state["episodes_so_far"]
        self.policy.set_weights(state["weights"])
        self.policy.set_filter(state["filter"])
        FilterManager.synchronize({
            DEFAULT_POLICY_ID: self.policy.get_filter()
        }, self.workers)
