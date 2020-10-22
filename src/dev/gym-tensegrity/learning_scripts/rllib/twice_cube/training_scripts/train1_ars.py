# This trained on only falling -> ARS_jumper_49096ce6_2020-02-22_12-24-34iew4vead 
import gym
import gym_tensegrity
import ray
from ray import tune

env_config = {'observation': ['nodes', 'nodes_velocities', 'rest_length']}

def create_environment(_):
    import gym_tensegrity
    return gym.make('gym_tensegrity:twice-cube-v0', config=env_config)

tune.register_env("twiceCube", create_environment)
ray.init()

tune.run(
        "ARS",
        name="train1_ars",
        stop={
            # "timesteps_total": 500000,#10000000,
            # 5000
            "episode_reward_mean": 1000,
        },
        checkpoint_freq=5,
        checkpoint_at_end=True,
        reuse_actors= True,
        config={
            "env": "twiceCube",
            "num_workers": 5,
            "ignore_worker_failures": True,
            "noise_stdev": 0.025,
            "num_rollouts": 100,#250,
            "rollouts_used": 50,#200,
            "sgd_stepsize": 0.03,
            "noise_size": 250000000,
            "eval_prob": 0.5,
            "env_config": env_config
        },
    )