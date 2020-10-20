import gym
import gym_tensegrity
import numpy as np
from timeit import default_timer as timer
import platform


config = {'observation': ['nodes', 'nodes_velocities', 'rest_length'],
          'render': False}

env = gym.make('gym_tensegrity:twice-cube-v0', config=config)

NUM_REPETITIONS = 5
NUM_TIMESTEPS = 4096

# With reset and environment creation
def full_time_forward():
    start = timer()
    env.reset()
    for _ in range(NUM_TIMESTEPS):
        action = env.action_space.sample()
        observation, reward, done, _= env.step(action)
    end = timer()
    
    return end - start

def no_reset_forward():
    start = timer()
    for _ in range(NUM_TIMESTEPS):
        action = env.action_space.sample()
        observation, reward, done, _= env.step(action)
    end = timer()
    
    return end - start


durations_full = []
durations_no_reset = []
for _ in range(NUM_REPETITIONS):
    durations_full.append(full_time_forward())

    env.reset()
    durations_no_reset.append(no_reset_forward())

print(f"Full-Time: Arch: {platform.machine()}; System: {platform.system()}; Num repetitions: {NUM_REPETITIONS}; Total: {np.mean(durations_full):.5f}s (+/- {np.std(durations_full):.5f}s); Per step: {np.mean(durations_full)/NUM_TIMESTEPS:.5f}s")
print(f"No-Reset: Arch: {platform.machine()}; System: {platform.system()}; Num repetitions: {NUM_REPETITIONS}; Total: {np.mean(durations_no_reset):.5f}s (+/- {np.std(durations_no_reset):.5f}s); Per step: {np.mean(durations_no_reset)/NUM_TIMESTEPS:.5f}s")