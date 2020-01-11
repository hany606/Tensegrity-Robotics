import gym_tensegrity
import gym
import ray
from ray import tune
import ray.rllib.agents.ppo as ppo


def create_environment(env_config):
    print(env_config.worker_index)
    import gym
    return gym.make('MountainCarContinuous-v0')

tune.register_env("mount", create_environment)

ray.init()

# Tune is easier way for running the algorithms and the configurations, instead of doing the follows
# But here is it straight forward for the modifications
# and tune is one of the libraries that are used to tune the hyperparameters and it is being used here for these two purposes, easy to train and tune
# From the documentation of RLlib: "It’s recommended that you run RLlib trainers with Tune, for easy experiment management and visualization of results."

# config = ppo.DEFAULT_CONFIG.copy()
# trainer = ppo.PPOTrainer(config=config, env="MountainCarContinuous-v0")

# # Can optionally call trainer.restore(path) to load a checkpoint.

# for i in range(1000):
#    # Perform one iteration of training the policy with PPO
#    result = trainer.train()
#    print(result)
# #    print(pretty_print(result))

#    if i % 100 == 0:
#        checkpoint = trainer.save()
#        print("checkpoint saved at", checkpoint)


tune.run(
    "PPO",
    stop={"episode_reward_mean": -30},
    config={
        "env": "mount",
        "num_gpus": 0,
        "num_workers": 1,
        # "lr": tune.grid_search([0.01, 0.001, 0.0001]),
        "eager": False,
    },
)