"""twice_cube_env.py: Create the gym custom environment of tensegrity TwiceCube tensegrity robot"""
__author__ = "Hany Hamed"
__credits__ = ["Hany Hamed"]
__version__ = "0.0.1"
__email__ = "h.hamed.elanwar@gmail.com / h.hamed@innopolis.university"
__status__ = "Developing"

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


import numpy as np
import math
from gym_tensegrity.envs.twice_cube_model import TwiceCubeModel

# Machine with Xscreen
path_to_model = os.path.join(os.environ["TENSEGRITY_HOME"], "build/dev/twiceCubeGym/AppTwiceCubeGymModel")
sim_exec_external = "gnome-terminal -e {}".format(path_to_model)

# Headless: to use it, change first in model file in startSimulation function
sim_exec_headless = path_to_model

class TwiceCubeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, config=None):
        if(config is not None):    
            self.config =  {
                            'host_name': 'localhost' if 'host_name' not in config.keys() else config['host_name'],
                            'port_num':None if 'port_num' not in config.keys() else config['port_num'],
                            'sim_exec': sim_exec_headless if 'sim_exec' not in config.keys() else config['sim_exec'],
                            'observation': ['nodes', 'nodes_velocities'] if 'observation' not in config.keys() else config['observation'],
                            'num_repeated_action': 1 if 'num_repeated_action' not in config.keys() else config['num_repeated_action'],
                            'max_num_steps': 20000 if 'max_num_steps' not in config.keys() else config['max_num_steps'],
                            'goal_coordinate': [12.0 ,-12.0 ,-12.0] if 'goal_coordinate' not in config.keys() else config['goal_coordinate'],
                            'done_threshold': 0.01 if 'done_threshold' not in config.keys() else config['done_threshold'],
                            'render': False if 'render' not in config.keys() else config["render"],
                            'error_threshold': 300 if 'error_threshold' not in config.keys() else config['error_threshold'],
                            }
        else:
            self.config =  {
                            'host_name': 'localhost',
                            'port_num':None,
                            'sim_exec':sim_exec_headless,
                            'observation': ['nodes', 'nodes_velocities'],
                            'num_repeated_action': 1,
                            'max_num_steps': 20000,
                            'goal_coordinate': [12.0, -12.0, -12.0],
                            'done_threshold': 0.01,
                            'render': False,
                            'error_threshold': 300,
                            }
        super(TwiceCubeEnv, self).__init__()

        if('nodes' not in self.config['observation'] and 'rest_length' not in self.config['observation'] and 'nodes_velocities' not in self.config['observation']):
            raise Exception("Wrong choice for the type of the observation, you should choose one of these [nodes, rest_length, current_length, nodes_velocities] or any option from them together in a form of list")

      
        if('sim_headless' in config.keys() and config['sim_headless'] == False):
            self.config = sim_exec_external
            self.config["sim_headless"] = False
        self.config["sim_headless"] = True 
        # Agent self variables
        self.max_cable_length = 1000
        self.min_coordinate = -200
        self.max_coordinate = -self.min_coordinate
        self.num_steps = 0
        self.max_num_steps = self.config['max_num_steps']
        self.goal_coordinate = self.config['goal_coordinate']
        self.done_threshold = self.config['done_threshold']
        self.error_threshold = self.config['error_threshold']

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


        self.observation_space = spaces.Box(low= low, high= high, dtype=np.float32)

    def __del__(self):
        self.env.closeSimulator()
    
    
    def step(self, action):
        self.num_steps += 1
        # This modification of multiple steps of actions was adapted from Atari environment: https://github.com/openai/gym/blob/master/gym/envs/atari/atari_env.py
        num_steps = 0
        num_repeated_action = self.config['num_repeated_action']
        rewards = 0
        
        if(self.num_steps == 1):
            self.initial_error = self._euclidean_distance_payload()
            print(f"Initial Error: {self.initial_error}")

        if isinstance(num_repeated_action, int):
            num_steps = num_repeated_action
        else:
            num_steps = randint(num_repeated_action[0], num_repeated_action[1])
        
        
        for _ in range(num_steps):    
            self._takeAction(action)
            observation = self._getObservation()
            rewards += self._getReward(observation)

        reward = rewards
        done = self._isDone()
        return observation, reward, done, {}

    # Continuous delta length
    # action is number that represents the length and the index of the controller
    # For example imaging that the delta_length = 10
    # Then if the action belongs to (-10,0]U[0,10) -- controller 0
    # action belongs to (-50,-40]U[40,50) -- controller 1
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

    # Observations:
    #   - The dimensions is specified above and their min. and max. values
    #   1- Nodes positions
    #   2- Nodes velocities
    #   3- Rest lengths of the cables
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
        reward = -1
        # reward = -self._euclidean_distance_payload()
        return reward

    def _isDone(self):
        #  The criteria for finish will be either
        #   if the payload reaches the specific coordinate or not within minimum error (threshold)
        euclidean_distance_payload = self._euclidean_distance_payload()
        if euclidean_distance_payload < self.done_threshold or self.num_steps > self.max_num_steps or euclidean_distance_payload > self.initial_error + self.error_threshold:
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
        self.env.render()

    def close(self):
        self.env.closeSimulator()
