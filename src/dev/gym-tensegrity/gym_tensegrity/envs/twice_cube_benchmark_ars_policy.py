import gym
import gym_tensegrity
import numpy as np

from timeit import default_timer as timer
import platform
import logging


import ray.rllib.agents.ars as ars
import ray
from ray import tune



config = {'observation': ['nodes', 'nodes_velocities', 'rest_length'],
          'render': False}

def create_environment(_):
    import gym_tensegrity
    return gym.make('gym_tensegrity:twice-cube-v0', config=config)

env = create_environment(None)

tune.register_env("twiceCube", create_environment)
ray.init(logging_level=logging.FATAL)

NUM_REPETITIONS = 5
NUM_TIMESTEPS = 4096

def ars_agent(agent_config={}, agent_file=None):
    config = ars.DEFAULT_CONFIG.copy()
    for key in agent_config.keys():
        config[key] = agent_config[key]
    config["num_workers"] = 1
    config["noise_size"] = 250000
    agent = ars.ARSTrainer(config, env="twiceCube")
    if(agent_file is not None):
        agent.restore(agent_file)
    return agent
# With reset and environment creation
def full_time_forward():
    agent = ars_agent()
    start = timer()
    observation = env.reset()
    for _ in range(NUM_TIMESTEPS):
        action = agent.compute_action(observation)
        # action = env.action_space.sample()    # Random sample
        observation, reward, done, _= env.step(action)
    end = timer()
    
    return end - start

def no_reset_forward(observation):
    agent = ars_agent()
    start = timer()
    for _ in range(NUM_TIMESTEPS):
        action = agent.compute_action(observation)
        # action = env.action_space.sample()    # Random sample
        observation, reward, done, _= env.step(action)
    end = timer()
    
    return end - start


durations_full = []
durations_no_reset = []
for _ in range(NUM_REPETITIONS):
    durations_full.append(full_time_forward())

    observation = env.reset()
    durations_no_reset.append(no_reset_forward(observation))

print(f"Full-Time: Arch: {platform.machine()}; System: {platform.system()}; Num repetitions: {NUM_REPETITIONS}; Total: {np.mean(durations_full):.5f}s (+/- {np.std(durations_full):.5f}s); Per step: {np.mean(durations_full)/NUM_TIMESTEPS:.5f}s")
print(f"No-Reset: Arch: {platform.machine()}; System: {platform.system()}; Num repetitions: {NUM_REPETITIONS}; Total: {np.mean(durations_no_reset):.5f}s (+/- {np.std(durations_no_reset):.5f}s); Per step: {np.mean(durations_no_reset)/NUM_TIMESTEPS:.5f}s")