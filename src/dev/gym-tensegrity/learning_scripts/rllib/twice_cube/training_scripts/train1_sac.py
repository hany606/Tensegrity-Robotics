# This trained on only falling -> ARS_jumper_49096ce6_2020-02-22_12-24-34iew4vead 
import gym
import gym_tensegrity
import ray
from ray import tune
import ray.rllib.agents.sac as sac
from ray.tune.logger import pretty_print


# For a reason that I don't understand for now, max_num_steps if it greater than a specific number (last experimented value: 2500), during the training the reward is nan for all the iterations
# Most probably because of "learning_starts" parameter inside SAC algorithm
env_config = {'observation': ['nodes', 'nodes_velocities', 'rest_length'], 'max_num_steps': 1000}


def create_environment(_):
    import gym_tensegrity
    return gym.make('gym_tensegrity:twice-cube-v0', config=env_config)
    # return gym.make('Pendulum-v0')
    # return gym.make('gym_tensegrity:test-v0')

tune.register_env("twiceCube", create_environment)
ray.init()



# def sac_agent():
#     config = sac.DEFAULT_CONFIG.copy()
#     agent = sac.SACTrainer(config, env="twiceCube")
#     return agent

# trainer = sac_agent()

# for i in range(1000):
#    # Perform one iteration of training the policy with PPO
#    result = trainer.train()
#    print(pretty_print(result))

#    if i % 100 == 0:
#        checkpoint = trainer.save()
#        print("checkpoint saved at", checkpoint)

tune.run(
        "SAC",
        name="train1_sac",
        stop={
            # "timesteps_total": 10000000,
            # 5000
            # "episode_reward_mean": -1000,
        },
        # checkpoint_freq=5,
        # checkpoint_at_end=True,
        # reuse_actors= True,
        config={
            "env": "twiceCube",
        },
    )


    # "Memory usage on this node: 7.1/7.5 GiB: ***LOW MEMORY*** less than 10% of the memory on this node is available for use. This can cause unexpected crashes. Consider reducing the memory used by your application or reducing the Ray object store size by setting `object_store_memory` when calling `ray.init`."