# This is the same as train3_mod_restore_train_random_ang3_2.py but with the modification in the library and the correlated and uncorelated noise as in the OpenAI paper of the manipulation hand to solve Rubik cube
# This is mixed of train4 and train5 with training for 1 angle
# train3_mod_restore_train_random_ang3_2.py trained on falling then angle 3 -> ARS_jumper_687731e0_2020-02-23_09-46-47ixwo7f1h

import gym
import gym_tensegrity
import ray
from ray import tune
from ars import ARSTrainer

env_config = {'observation': ['end_points', 'end_points_velocities', 'rest_length'], 'control_type': 'rest_length_mod', 'starting_coordinates':[0,10,0],  "extra_trainer_configs": {"domain_randomization":{"starting_leg_angle":{"min":[0,-3], "max":[0,3]}}}}

def create_environment(_):
    import gym_tensegrity
    # return gym.make('gym_tensegrity:jumper-v0', config=config)
    return gym.make('gym_tensegrity:jumper-v0', config=env_config)

env_config["extra_trainer_configs"].update(
                {"num_randomized_envs":16})

env_config['observation_noise'] = {
    "uncorrelated":{"mean":0,"stdev":1},
    "correlated":{"mean":0,"stdev":1}
}

tune.register_env("jumper", create_environment)
ray.init()

tune.run(
        ARSTrainer,
        name="train6_ground_random_ang3_leg_angle_restore_train_mod_lib_observation_noise",
        restore="/root/ray_results/train3_restore_train_ang3/ARS_jumper_f573b3a8_2020-02-16_22-37-4865ib9uls/checkpoint_760/checkpoint-760",
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