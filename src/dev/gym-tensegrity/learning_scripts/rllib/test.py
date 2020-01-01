import gym_tensegrity
import gym
import ray
from ray import tune

def create_environment(env_config):
    import gym_tensegrity
    return gym.make('gym_tensegrity:jumper-v0')

tune.register_env("Jumper", create_environment)

ray.init()

tune.run(
        "ARS",
        stop={
            "timesteps_total": 10000,
        },
        config={
            "env": "Jumper",
        },
    )
