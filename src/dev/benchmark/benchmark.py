import numpy as np
from timeit import default_timer as timer
import gym_tensegrity

NUM_REPETITIONS = 5

env = gym.make('gym_tensegrity:twice-cube-v0')


# With reset and environment creation
def full_time_forward():
    start = timer()
    env.reset()
    for _ in range(env.num_timesteps):
        env.step()
    end = timer()
    
    return end - start

def no_reset_forward():
    start = timer()
    for _ in range(env.num_timesteps):
        env.step()
    end = timer()
    
    return end - start


durations_full = []
durations_no_reset = []
for _ in range(NUM_REPETITIONS):
    durations_full.append(full_time_forward())

    env.reset()
    durations_no_reset.append(no_reset_forward())

print(f"Full-Time: Arch: {ARCH}; Num repetitions: {NUM_REPETITIONS}; Total: {np.mean(durations_full):.5f}s (+/- {np.std(durations_full):.5f}s); Per step: {np.mean(durations_full)/4096:.5f}s")
print(f"No-Reset: Arch: {ARCH}; Num repetitions: {NUM_REPETITIONS}; Total: {np.mean(durations_no_reset):.5f}s (+/- {np.std(durations_no_reset):.5f}s); Per step: {np.mean(durations_no_reset)/4096:.5f}s")
