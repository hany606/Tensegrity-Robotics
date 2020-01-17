import gym
import gym_tensegrity
import ray
from ray import tune
import ray.rllib.agents.ars as ars
from ray.tune.logger import pretty_print


def create_environment(env_config):
    import gym_tensegrity
    return gym.make('gym_tensegrity:jumper-v0', config={'observation':'end_points', "control_type": 'rest_length_mod'})

tune.register_env("jumper", create_environment)
ray.init()

# analysis = tune.run(
#         "ARS",
#         name="test_save_model",
#         stop={
#             "timesteps_total": 10000,
#         },
#         verbose=2,
#         checkpoint_at_end=True,
#         reuse_actors= True,
#         config={
#             "env": "jumper",
#             "num_workers": 10,
#             "noise_stdev": 0.02,
#             "num_rollouts": 30,
#             "rollouts_used": 30,
#             "sgd_stepsize": 0.01,
#             "noise_size": 250000000,
#             "eval_prob": 0.09,
#             # "num_envs_per_worker":1,
#         },
#     )

config = ars.DEFAULT_CONFIG.copy()
config["num_workers"] = 1
config["noise_stdev"] = 0.02
config["num_rollouts"] = 100
config["rollouts_used"] = 50
config["sgd_stepsize"] = 0.03
config["noise_size"] = 250000000
config["eval_prob"] = 0.5
#config["env_config"] = {"observation":'end_points', "control_type":'current_length_mod'}
#restore_model_path = "evaluate/ARS_jumper_15f133ce_2020-01-13_18-04-04oajwg41_/checkpoint_210/checkpoint-210"
restore_model_path = "evaluate/checkpoint_180/checkpoint-180"

##tune.run("ARS", restore=restore_model_path, stop={"timesteps_total": 100000}, config={"env": "jumper"})



test_agent = ars.ARSTrainer(config, env="jumper")

test_agent.restore(restore_model_path)
env = create_environment("a")
for i in range(50):
    state = env.reset()
    cumulative_reward = 0
    done  = False
    #print(cumulative_reward)
    while not done:
        action = test_agent.compute_action(state)
        #print(action)
        #action = env.action_space.sample()
        state, reward, done, _ = env.step(action)
        cumulative_reward += reward
    print("%#%#%#%#%#%Total Reward: {:}".format(cumulative_reward))
    #break
    #input("!@@!#INPUT")
# print("*-*-*-*-*--*-**-*-*-*-*-*-*-*-*--*-*---*--*-*-*-*-*--*-*--*-*-*--*-")
# for i in analysis.trials:
#     print(i)
# # print(analysis.trials)
# print("*-*-*-*-*--*-**-*-*-*-*-*-*-*-*--*-*---*--*-*-*-*-*--*-*--*-*-*--*-")
