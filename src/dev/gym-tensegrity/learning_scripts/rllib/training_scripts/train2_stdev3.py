import gym
import gym_tensegrity
import ray
from ray import tune

env_config = {'observation': ['end_points', 'end_points_velocities'], 'control_type': 'rest_length_mod', 'starting_coordinates':(0,10,0), 'randomized_starting': True}

def create_environment(_):
    import gym_tensegrity
    # return gym.make('gym_tensegrity:jumper-v0', config=config)
    return gym.make('gym_tensegrity:jumper-v0', config=env_config)

tune.register_env("jumper", create_environment)
ray.init()
tune.run(
        "ARS",
        name="train_025_rep_act1_restL_randomized_starting_3_degree_1_axis_on_ground_after_correct_randomization_std3",
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
            "noise_stdev": 0.08,
            "num_rollouts": 100,
            "rollouts_used": 50,
            "sgd_stepsize": 0.03,
            "noise_size": 250000000,
            "eval_prob": 0.5,
            "env_config": env_config
        },
    )