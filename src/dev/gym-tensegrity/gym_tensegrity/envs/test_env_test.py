import gym
import gym_tensegrity
import numpy as np
import os
from time import sleep

def test(config=None):
    def print_observation(obs):
        # This printing for the default observation
        print("Observations: ")
        print(obs)    
    env = gym.make('gym_tensegrity:test-v0')
    observation = env.reset()
    print_observation(observation)
    tot_reward = 0
    done = False

    steps = 0
    while not done:
        #inp = input("INPUT")
        steps += 1
        action = env.action_space.sample()
        # action = [0 for i in action]
        # action[0  ] = 1
        # action[:4] = [0.001 for i in range(4)]
        # action[4:] = [-0.001 for i in range(4)]
        action = np.array(action)
        # print("Action: {:}".format(action))
        observation, reward, done, _= env.step(action)
        # print(len(observation))
        tot_reward += reward
        print("Reward: {:}, Done: {:}".format(reward,done))
        # print_observation(observation)
        print("Total Reward: {:}".format(tot_reward))
        print("-------------------------------------------------")
    print(f"Total number of steps: {steps}")

if __name__ == "__main__":
    test()