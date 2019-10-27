#using stable-baselines
import gym_tensegrity

import gym
from gym import wrappers
import random
import numpy as np
import matplotlib.pyplot as plt

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

env = gym.make('gym_tensegrity:leg-v0')
# env = wrappers.Monitor(env, 'CartPole_q_learning_video', force=True)

env = DummyVecEnv([lambda: env])

model = DQN(MlpPolicy, env, verbose=1)
# model.learn(total_timesteps=25000)
model.save("deepq_tensegrity_leg")

# # del model # remove to demonstrate saving and loading

model = DQN.load("deepq_tensegrity_leg")

obs = env.reset()
done  = False
while not done:
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    # print(obs)
    env.render()