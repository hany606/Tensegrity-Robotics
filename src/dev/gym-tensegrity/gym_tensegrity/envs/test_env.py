# This file will contain all the information about the agent and the environment starting from the rendering of the GUI to the rewards,... etc.
import os
import time
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import sys
import signal
from math import floor,log2, sqrt
import logging
from random import randint,uniform
from gym_tensegrity.envs.twice_cube_model import TwiceCubeModel


import numpy as np
import math

path_to_model = os.path.join(os.environ["TENSEGRITY_HOME"], "build/dev/twiceCubeGym/AppTwiceCubeGymModel")
sim_exec_headless = path_to_model


class TestEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(TestEnv, self).__init__()
        # self.action_space = spaces.Box(low=np.full((2,), -1), high=np.full((2,), 1), dtype=np.float32)
        # self.observation_space = spaces.Box(low=np.full((4,), -10), high=np.full((4,), 10), dtype=np.float32)    
        # self.num_steps = 0

        self.config = {'host_name': 'localhost',
                           'port_num': None,
                           'sim_exec': sim_exec_headless,
                           'observation': ['nodes', 'nodes_velocities', 'rest_length'],
                           'num_repeated_action': 1,
                           'max_num_steps':1000,
                           'goal_coordinate': [12.0, -12.0, -12.0],
                           'done_threshold': 0.01,
                           'render': False,
                           'error_threshold': 300,
                           'max_reward': 500,
                           'sim_headless': True}
        super(TestEnv, self).__init__()

        if(not(set(self.config['observation']).issubset(set(['nodes', 'rest_length', 'nodes_velocities'])))):
            raise Exception("Wrong choice for the type of the observation, you should choose one of these [nodes, rest_length, nodes_velocities] or any option from them together in a form of list")
      
        # Agent self variables
        self.max_cable_length = 1000
        self.min_coordinate = -200
        self.max_coordinate = -self.min_coordinate
        self.num_steps = 0
        self.max_num_steps = self.config['max_num_steps']
        self.goal_coordinate = self.config['goal_coordinate']
        self.done_threshold = self.config['done_threshold']
        self.error_threshold = self.config['error_threshold']
        self.max_reward = self.config['max_reward']

        # self.starting_coordinates[1] = 10.535 # starting_coordinates [y,z,x]
        self.env = TwiceCubeModel(host_name=self.config['host_name'], port_num=self.config['port_num'],
                                  sim_exec=self.config['sim_exec'], render_flag=self.config["render"], sim_headless=self.config["sim_headless"])
        self.nodes_num = self.env.nodes_num - 8 + 1 # Only the active nodes are all the nodes except the last 8 which will be used to generate the payload node

        self.env.startSimulator()

        # Continuous Action space for the delta lengths
        self.delta_length = 2

        self.min_node_velocity = -2000
        self.max_node_velocity = -self.min_node_velocity

        low = np.array([-1*self.delta_length for i in range(self.env.controllers_num)])
        high = np.array([self.delta_length for i in range(self.env.controllers_num)])
        self.action_space = spaces.Box(low=low, high=high, dtype=np.float32)

        low = np.empty((1,0))
        high = np.empty((1,0))

        if('nodes' in self.config['observation']):
            low = np.append(low, np.full((1,self.nodes_num*3), self.min_coordinate))
            high = np.append(high, np.full((1,self.nodes_num*3), self.max_coordinate))

        if('nodes_velocities' in self.config['observation']):
            low = np.append(low, np.full((1,self.nodes_num*3), self.min_node_velocity))
            high = np.append(high, np.full((1,self.nodes_num*3), self.max_node_velocity))

        
        if('rest_length' in self.config['observation']):
            # low = np.append(low, self.min_leg_angle)
            low = np.append(low, np.zeros(self.env.controllers_num))
            # high = np.append(high, self.max_leg_angle)
            high = np.append(high, np.full((1,self.env.controllers_num), self.max_cable_length))

        # self.action_space = spaces.Box(low=np.full((self.env.controllers_num,), -self.delta_length), high=np.full((self.env.controllers_num,), self.delta_length), dtype=np.float32)
        self.observation_space = spaces.Box(low= low, high= high, dtype=np.float32)


    def step(self, action):
        self.num_steps += 1
        if(self.num_steps == 1):
            self.initial_distance = self._euclidean_distance_payload()
            print(f"Initial Error: {self.initial_distance}")

        self._takeAction(action)
        observation = self._getObservation()
        reward = self._getReward(observation)
        done = self._isDone()
        return observation, reward, done, {}

    def _takeAction(self, action):
        if (not isinstance(action, np.ndarray)):
            raise Exception("The action space should be an np.array")
        if action.shape != self.action_space.shape:
            raise Exception("The shape of the provided action does not match")
        
        action = np.clip(action,-self.delta_length, self.delta_length)
        # This is now useless after the value clipping
        if not self.action_space.contains(action):
            raise Exception("The provided action is out of allowed space.")

        self.env.actions_json["controllers_val"][:] = action.tolist()
        self.env.step()

    def _getObservation(self):
        observation = np.empty((1,0))

        if('nodes' in self.config['observation']):
            for i in self.env.getNodes():
                observation = np.append(observation, i)

        if('nodes_velocities' in self.config['observation']):
            observation = np.append(observation, self.env.getNodesVelocities())

        if('rest_length' in self.config['observation']):
            # observation = np.append(observation, self.env.getLegAngle())
            observation = np.append(observation, self.env.getRestCablesLengths())

        return np.array(observation)


    def _euclidean_distance(self, obs1, obs2):
        euclidean_distance_part = lambda x1, x2: (x1-x2)**2
        euclidean_distance = (sum([euclidean_distance_part(obs1[i], obs2[i]) for i in range(len(obs1))]))/2
        return euclidean_distance

    def _euclidean_distance_payload(self):
        return self._euclidean_distance(self.env.getPayLoad()[0], self.goal_coordinate)

    # Reward criteria
    def _getReward(self, observation):
        # Reward Criteria will depend on:
        #   We need to minimize the time to reach the goal point
        #       Negative reward depends on the time that been 
        # reward = -1
        # To make negative correlate with positive rewards
        # euclidean_distance = self._euclidean_distance_payload()
        # reward = self.max_reward/(euclidean_distance+1)

        reward = -self._euclidean_distance_payload()/self.initial_distance
        return reward

    def _isDone(self):
        #  The criteria for finish will be either
        #   if the payload reaches the specific coordinate or not within minimum error (threshold)
        euclidean_distance_payload = self._euclidean_distance_payload()
        if euclidean_distance_payload < self.done_threshold or euclidean_distance_payload > self.initial_distance + self.error_threshold or self.num_steps > self.max_num_steps:
                self.num_steps = 0
                return True
        return False

    def reset(self):
        # Reset the state of the environment to an initial state, and the self vars to the initial values
        self.num_steps = 0

        # Reset the environment and the simulator
        self.env.reset()
        self.env.step()
        # Not necessary as long as we didn't comment it in the _takeAction above
        for i in range(self.env.controllers_num):
            self.env.actions_json["controllers_val"][i] = 0

        # get the observations after the resetting of the environment
        return self._getObservation()

    def render(self, mode='human'):
        pass
    def close(self):
        pass