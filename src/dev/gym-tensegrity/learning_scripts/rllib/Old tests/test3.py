import gym
import gym_tensegrity
import ray
from ray import tune

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

# @static_vars(counter=0)
def create_environment(env_config):
    # config = {'port_num': 10000+create_environment.counter}
    # create_environment.counter += 1
    import gym_tensegrity
    # return gym.make('gym_tensegrity:jumper-v0', config=config)
    return gym.make('gym_tensegrity:jumper-v0', config={'observation':'rest_length'})


# Gives errors as env_config is empty but in the documentation it shouldn't
# https://ray.readthedocs.io/en/latest/rllib-env.html#configuring-environments
# class MultiEnvPorts(gym.Env):
#     def __init__(self, env_config):
#         import gym_tensegrity
#         print("----------------------------------------------------------------/**//*/*/")
#         print(env_config)
#         self.config = {'port_num': 1000+env_config.worker_index}
#         self.env = gym.make('gym_tensegrity:jumper-v0', config=self.config)
#     def reset(self):
#         return self.env.reset()
#     def step(self, action):
#         return self.env.step(action)

tune.register_env("jumper", create_environment)
ray.init()
# tune.register_env("Jumper", lambda config: MultiEnvPorts(config))
analysis = tune.run(
        "ARS",
        name="long_Train",
        stop={
            "timesteps_total": 1000000,
        },
        verbose=2,
        checkpoint_freq=5,
        checkpoint_at_end=True,
        reuse_actors= True,
        config={
            "env": "jumper",
            "num_workers": 10,
            "noise_stdev": 0.02,
            "num_rollouts": 50,
            "rollouts_used": 30,
            "sgd_stepsize": 0.03,
            "noise_size": 250000000,
            "eval_prob": 0.5,
            # "num_envs_per_worker":1,
        },
    )

# print("*-*-*-*-*--*-**-*-*-*-*-*-*-*-*--*-*---*--*-*-*-*-*--*-*--*-*-*--*-")
# for i in analysis.trials:
#     print(i)
# # print(analysis.trials)
# print("*-*-*-*-*--*-**-*-*-*-*-*-*-*-*--*-*---*--*-*-*-*-*--*-*--*-*-*--*-")
