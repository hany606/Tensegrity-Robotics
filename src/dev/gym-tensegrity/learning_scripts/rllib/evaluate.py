import gym
import gym_tensegrity
import ray
from ray import tune
import ray.rllib.agents.ars as ars
from ray.tune.logger import pretty_print


def create_environment(env_config):
    import gym_tensegrity
    return gym.make('gym_tensegrity:jumper-v0', config={'observation':'rest_length'})

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
config["num_rollouts"] = 50
config["rollouts_used"] = 30
config["sgd_stepsize"] = 0.03
config["noise_size"] = 250000000
config["eval_prob"] = 0.5

#restore_model_path = "evaluate/ARS_jumper_15f133ce_2020-01-13_18-04-04oajwg41_/checkpoint_210/checkpoint-210"
restore_model_path = "evaluate/checkpoint_15/checkpoint-15"

##tune.run("ARS", restore=restore_model_path, stop={"timesteps_total": 100000}, config={"env": "jumper"})
trainer = ars.ARSTrainer(config=config, env="jumper")

trainer.restore(restore_model_path)

for i in range(10):
   # Perform one iteration of training the policy with PPO
   result = trainer.train()
   print(pretty_print(result))
# print("*-*-*-*-*--*-**-*-*-*-*-*-*-*-*--*-*---*--*-*-*-*-*--*-*--*-*-*--*-")
# for i in analysis.trials:
#     print(i)
# # print(analysis.trials)
# print("*-*-*-*-*--*-**-*-*-*-*-*-*-*-*--*-*---*--*-*-*-*-*--*-*--*-*-*--*-")
