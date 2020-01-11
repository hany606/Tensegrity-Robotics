import gym_roboticArm

# Purpose is to develop QLearning algorithm with CartPole environment
import gym
import numpy as np
from tqdm import tqdm
import os
from time import sleep
import tensorflow as tf
import matplotlib.pyplot as plt
from random import random

# env = gym.make("CartPole-v0")
env = gym.make('roboticArm-v0')

# Actions, Observations & rewards of CartPole:  https://github.com/openai/gym/wiki/CartPole-v0

# Table Method
# Parameters of learning (hyper-parameters)
learning_rate = 0.5
discount = 0.2
num_training_episodes = 100
num_testing_episodes = 10
episode_lifetime = 100


# 1- Change the values from continuous to discrete values
# 2- Create Q-table with the specific dimensions and sizes
# 3- Fill the Q-table using MC (random actions)
# 4- Use the Q-table for some test episodes

def to_discrete(observation):
    lower = [env.observation_space.low[0], env.observation_space.low[1]]
    upper = [env.observation_space.high[0], env.observation_space.high[1]]
    step = [0.05, 0.05]

    bins = [np.linspace(lower[i], upper[i], num=(upper[i]-lower[i])/step[i]+1)[1:-1] for i in range(2)]
    # for i in range(2):
    #     print(lower[i], upper[i])
    #     print(env.observation_space.low[i], env.observation_space.high[i])
    #     print(len(bins[i]))
    discrete_observation = [np.digitize(observation[i], bins[i]) for i in range(2)]
    return discrete_observation

# def to_discrete_action(action):
#     lower = [env.action_space.low[0], env.action_space.low[1]]
#     upper = [env.action_space.high[0], env.action_space.high[1]]
#     step = [0.5, 0.5]
#
#     bins = [np.linspace(lower[i], upper[i], num=(upper[i]-lower[i])/step[i]+1)[1:-1] for i in range(2)]
#     # for i in range(2):
#         # print(lower[i], upper[i])
#         # print(env.observation_space.low[i], env.observation_space.high[i])
#         # print(len(bins[i]))
#     discrete_action = [np.digitize(action[i], bins[i]) for i in range(2)]
#     return discrete_action

# def to_cont_action(action):
#     lower = [env.action_space.low[0], env.action_space.low[1]]
#     upper = [env.action_space.high[0], env.action_space.high[1]]
#     step = [0.5, 0.5]
#
#     bins = [np.linspace(lower[i], upper[i], num=(upper[i]-lower[i])/step[i]+1)[1:-1] for i in range(2)]
#     # print(len(bins[0]))
#     # print(action)
#     cont_action = [(bins[i][min(len(bins[i])-1,action[i])]+bins[i][min(len(bins[i])-1,action[i]+1)])/2 for i in range(2)]
#     return cont_action

# obs = [0, 0]
# print(to_discrete(obs))
# exit()
if not os.path.exists("roboticArm_Q_table.npy"):
    print("Creating a new Q-table")
    Q_table = np.zeros((8000, 8000, 9))
else:
    print("Loading an existing Q-table")
    Q_table = np.load("roboticArm_Q_table.npy")
# print(Q_table.shape)
# print(Q_table.size)
# print(Q_table.ndim)


reward_list = []
for episode in tqdm(range(num_training_episodes)):

    observation = env.reset()

    reward_all = 0
    done = False
    for step in range(episode_lifetime):
        # Take a random action
        # action = round(random())

        action = env.action_space.sample()
        new_observation, reward, done, _ = env.step(action)
        observation_discrete = to_discrete(observation)
        new_observation_discrete = to_discrete(new_observation)
        # print(action, reward)

        # print(observation_discrete, action_discrete)
        # Filling the Q-Table
        # Q_table[0, 0, 0] += reward
        # print(observation_discrete, action)
        Q_table[observation_discrete[0], observation_discrete[1], action] += reward
        Q_table[observation_discrete[0], observation_discrete[1], action] += \
            learning_rate * (
                    reward + discount * np.max(
                Q_table[new_observation_discrete[0], new_observation_discrete[1], :])
                    - Q_table[
                        observation_discrete[0], observation_discrete[1], action])
        reward_all += reward
        observation = new_observation

        if done:
            break
    reward_list.append(reward_all)

# for i1 in range(800):
#     for i2 in range(800):
#         for i in range(9):
#             print(Q_table[i1][i2][i],end=", ")
#         print("\n")
#     print("\n")

print("Score over time: {:}".format(sum(reward_list) / num_training_episodes))
print('\n---------------------------\n')
print(Q_table)
print('\n---------------------------\n')
# input("Continue (y/y) ??")
plt.plot(reward_list, color='b')

# np.save("roboticArm_Q_table", Q_table)

reward_list = []
for episode in range(num_testing_episodes):
    observation = env.reset()
    episode_reward = 0
    done = False
    for steps in range(episode_lifetime):
        # env.render()
        observation_discrete = to_discrete(observation)
        action = np.argmax(
            Q_table[observation_discrete[0], observation_discrete[1], :])

        # action = [action0_discrete[0], action1]
        # print(action)

        # action_cont[0] = action0[0]
        # print(action_cont)
        # clear()
        # print(Q[observation, :])
        # print("Episode: {:}".format(i))
        # print("Action: {:}".format(action))
        new_observation, reward, done, _ = env.step(action)
        # print("Reward {:} at step: {:}".format(reward, steps+1))
        observation = new_observation
        episode_reward += reward

        env.render()
        sleep(0.01)

        if done:
            print("Reward of the episode {:} = {:}".format(episode+1, episode_reward))
            # sleep(2)
            env.render()
            sleep(2)
            # env.close()
            break
    if not done:
        print("---Exceed the lifetime -- reward of the episode {:} = {:}".format(episode + 1, episode_reward))
    reward_list.append(episode_reward)
    # print("-----------------------")

print("Average score over time: {:}".format(sum(reward_list) / num_testing_episodes))

plt.plot(reward_list, color='r')

plt.show()

# env.step([np.pi,0])
#
#
# while(1):
#     env.render()

# NN Method
