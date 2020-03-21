import gym
import gym_tensegrity
import ray
from ray import tune

env_config = {'observation': ['end_points', 'end_points_velocities', 'rest_length'], 'control_type': 'rest_length_mod', 'starting_coordinates':[0,10,0], "randomized_starting": {"angle":[[True,True], [-3,-3], [3,3]], "height":[False]}}

def create_environment(_):
    import gym_tensegrity
    # return gym.make('gym_tensegrity:jumper-v0', config=config)
    return gym.make('gym_tensegrity:jumper-v0', config=env_config)

tune.register_env("jumper", create_environment)
ray.init()
tune.run(
        "ARS",
        name="train3_hp(mod_increased_rollouts)_ground_random_2angles3_leg_angle_restore_train",
        restore="/root/ray_results/train3_hp(mod_increased_rollouts)_ground_random_ang3_leg_angle_restore_train/ARS_jumper_687731e0_2020-02-23_09-46-47ixwo7f1h/checkpoint_1040/checkpoint-1040",
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
            "rollouts_used": 200,
            "sgd_stepsize": 0.03,
            "noise_size": 250000000,
            "eval_prob": 0.5,
            "env_config": env_config
        },
    )