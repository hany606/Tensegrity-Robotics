"""DQN.py: Implementation for DQN algorithm with gym_leg"""
__author__ = "Hany Hamed"
__credits__ = ["Hany Hamed", "Prof. Sergie Savin", "Innopolis University"]
__version__ = "0.0.1"
__email__ = "h.hamed.elanwar@gmail.com / h.hamed@innopolis.university"
__status__ = "Developing"




# Sources:
# https://lilianweng.github.io/lil-log/2018/05/05/implementing-deep-reinforcement-learning-models.html
# https://github.com/lilianweng/deep-reinforcement-learning-gym/blob/master/playground/policies/dqn.py
# https://github.com/devsisters/DQN-tensorflow


import gym_tensegrity

import gym
from gym import wrappers
import random
import numpy as np
import matplotlib.pyplot as plt


# Parameters
learning_rate = 0.5
discount = 0.2
num_training_episodes = 100
num_testing_episodes = 10
episode_lifetime = 100

# Initial variables
env = gym.make('gym_tensegrity:leg-v0')


# Helper functions



# Deep Q-Network algorithm


# Double Q-Network algorithm


# Dueling Q-Network algorithm





# Training




# Testing



# Main
def main():
    pass


if __name__ == "__main__":
    main()