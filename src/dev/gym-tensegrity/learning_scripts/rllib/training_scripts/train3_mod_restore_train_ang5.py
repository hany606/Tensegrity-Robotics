import gym
import gym_tensegrity
import ray
from ray import tune

env_config = {'observation': ['end_points', 'end_points_velocities', 'rest_length'], 'control_type': 'rest_length_mod', 'starting_coordinates':(0,10,0), 'starting_leg_angle': (5,0)}

def create_environment(_):
    import gym_tensegrity
    # return gym.make('gym_tensegrity:jumper-v0', config=config)
    return gym.make('gym_tensegrity:jumper-v0', config=env_config)

tune.register_env("jumper", create_environment)
ray.init()
tune.run(
        "ARS",
        name="train3_restore_train_ang5",
        restore="/root/ray_results/train3_restore_train_ang3/ARS_jumper_f573b3a8_2020-02-16_22-37-4865ib9uls/checkpoint_705/checkpoint-705",
        stop={
            # "timesteps_total": 10000000,
            # 5000
            "episode_reward_mean": 20000,
        },
        checkpoint_freq=5,
        checkpoint_at_end=True,
        reuse_actors= True,
        config={
            "env": "jumper",
            "num_workers": 10,
            "ignore_worker_failures": True,
            "noise_stdev": 0.025,
            "num_rollouts": 250,
            "rollouts_used": 100,
            "sgd_stepsize": 0.03,
            "noise_size": 250000000,
            "eval_prob": 0.5,
            "env_config": env_config
        },
    )
    