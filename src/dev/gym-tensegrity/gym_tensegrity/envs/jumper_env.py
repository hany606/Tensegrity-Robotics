"""jumper_env.py: Create the gym custom environment of tensegrity one legged jumpeing robot"""
__author__ = "Hany Hamed"
__credits__ = ["Hany Hamed", "Vlad Kurenkov", "Prof. Sergie Savin", "Oleg Balakhnov"]
__version__ = "0.0.1"
__email__ = "h.hamed.elanwar@gmail.com / h.hamed@innopolis.university"
__status__ = "Developing"

# ----------------------------------------------------------------------------------------
# Problems that undetermined: [TODO]
# 
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Modifications from previous version:
# 
# ----------------------------------------------------------------------------------------






# This file will contain all the information about the agent and the environment starting from the rendering of the GUI to the rewards,... etc.
import os
import time
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import sys
import signal
from math import floor,log2
import logging
from random import randint,uniform

# logger = logging.getLogger(__name__)

import numpy as np
import math
from gym_tensegrity.envs.jumper_model import JumperModel

# Machine with Xscreen
path_to_model = os.path.join(os.environ["TENSEGRITY_HOME"], "build/dev/jumper/AppJumperModel")
sim_exec = "gnome-terminal -e {}".format(path_to_model)

#Headless
# sim_exec = '/home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/build/dev/jumper/AppJumperModel'

class JumperEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, config=None):
        if(config is not None):    
            self.config =  {
                            'host_name': 'localhost' if 'host_name' not in config.keys() else config['host_name'],
                            'port_num':10042 if 'port_num' not in config.keys() else config['port_num'],
                            'sim_exec':sim_exec if 'sim_exec' not in config.keys() else config['sim_exec'],
                            'dl':0.1 if 'dl' not in config.keys() else config['dl']
                            }
        else:
            self.config =  {
                            'host_name': 'localhost',
                            'port_num':10042,
                            'sim_exec':sim_exec,
                            'dl':0.1
                            }

        super(JumperEnv, self).__init__()
        # Agent self variables
        self.max_time = 200
        self.max_cable_length = 50
        self.min_leg_angle = -np.pi/2
        self.max_leg_angle =  np.pi/2
        self.dl = self.config['dl']
        
        self.env = JumperModel(host_name=self.config['host_name'], port_num=self.config['port_num'], sim_exec=self.config['sim_exec'], dl=self.config['dl'])
        self.env.startSimulator()

        # Discrete Action space
        # 3 bits for indexing the cable's controller 2^3 = 8 and one bit for the control direction
        # This action space will inforce to have only one working controller at a time
        # Also, always one controller work at least there is no possibilty to have all of them not working, to aoid this point we can add another bit fot the control direction 
        # n_actions = 2**(floor(log2(self.env.controllers_num))+1)
        # self.action_space = spaces.Discrete(n_actions)
        
        # Continuous Action space for the lengths
        # low = np.array([0 for i in range(self.env.controllers_num)])
        # high = np.array([self.max_cable_length for i in range(self.env.controllers_num)])
        # self.action_space = spaces.Box(low=low, high=high, dtype=np.float32)

        # Continuous Action space for the delta lengths
        self.delta_length = 2 

        # low = np.array(-1*self.delta_length*self.env.controllers_num)
        # high = np.array(-1*low)
        # self.action_space = spaces.Box(low=low, high=high, dtype=np.float32)

        low = np.array([-1*self.delta_length for i in range(self.env.controllers_num)])
        high = np.array([self.delta_length for i in range(self.env.controllers_num)])
        self.action_space = spaces.Box(low=low, high=high, dtype=np.float32)

        low = np.array(self.min_leg_angle)
        low = np.append(low, np.zeros(self.env.controllers_num))

        high = np.array(self.max_leg_angle)
        high = np.append(high, np.full((1,self.env.controllers_num), self.max_cable_length))
 
        self.observation_space = spaces.Box(low= low, high= high, dtype=np.float32)

        # To randomize the initial state of the strings
        # random_init_lengths = [((1 if randint(1,10)%2 else -1)*uniform(self.delta_length-1, self.delta_length)) for i in range(self.env.controllers_num)]
        # self.env.actions_json["Controllers_val"][:] = random_init_lengths
        # self.env.step()



    def __del__(self):
        self.env.closeSimulator()
            
    def step(self, action):
        self._takeAction(action)
        observation = self._getObservation()
        reward = self._getReward(observation)
        done = self._isDone()
        return observation, reward, done, {}

    # # Discrete
    # # 3 bits for the index of the cable, 1 bit (the last one) for the direction of the controller (increase or decrease)
    # def _takeAction(self, action):
    #     bits_num = floor(log2(self.env.controllers_num))+1
    #     value_sign = (1 if ((2**(bits_num-1)) & action) > 0 else -1)    # if sign_bit is 0 = decrease, 1 = increase
    #     value = value_sign*self.dl
    #     # print(self.env.controllers_num)
    #     # controller_index = action - (2**(bits_num-1) if value_sign == 1 else 0)
    #     controller_index = action%(2**(bits_num-1))
    #     # print("Controllers_index {:} :::{:}, Controller_value: {:}".format(controller_index, action, value))
        
    #     # TODO: Don't know if it is necessary or not. Maybe here we can set all the controllers to zero and delete the last line in the method
    #     self.env.actions_json["Controllers_val"][controller_index] = value
    #     self.env.step()
    #     self.env.actions_json["Controllers_val"][controller_index] = 0    # IF we comment that, this will enable the environment to operate simultanously actuators

    # Continuous length
    # action is vector of continuous values for the controllers of the strings
    # def _takeAction(self, action):
    #     if(isinstance(action, np.ndarray)):
    #         action_list = action.tolist()
    #     else:
    #         action_list = action
    #     self.env.actions_json["Controllers_val"][:] = action_list
    #     self.env.step()

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

        if not self.action_space.contains(action):
            raise Exception("The provided action is out of allowed space.")

        self.env.actions_json["Controllers_val"][:] = action.tolist()
        # The commented part is for take only one value and decide the controller index and the value from it not vector of actions
        # # print(action, type(action))
        # controller_index = abs(action)//self.delta_length
        # value = (1 if action > 0 else -1)*abs(action)%self.delta_length
        # if(action == -1*self.delta_length*self.env.controllers_num or action == self.delta_length*self.env.controllers_num):
        #         controller_index = self.env.controllers_num-1
        #         value = (1 if action > 0 else -1)*self.delta_length
        # # print("TAke action")
        # # print("debug", 11.1272207%self.delta_length)
        # # print(controller_index, value, action)
        # self.env.actions_json["Controllers_val"][int(controller_index)] = float(value)
        self.env.step()

    # Observations:
    #   - The dimensions is specified above and their min. and max. values
    #   1- Angle of the leg
    #   2- Cables' lengths
    def _getObservation(self):
        observation = np.empty((1,0))
        observation = np.append(observation, self.env.getLegAngle())
        observation = np.append(observation, self.env.getCablesLengths())
        # print("finish getting the observation")
        return np.array(observation)

    def _getReward(self, observation):
        # Reward Criteria will depend on:
        #   - The angle of the leg
        #   - The time
        time = self.env.getTime()
        # The coefficient of the the time has been calculated according to y = ct and having t_max= 200, y_max= 4 (the maximum reward that can be gained)
        # The total reward from the time that can be gained will be 400 (using the integration) 
        
        # I multiplied the factor in 10 to increase the negative reward
        return 0.02*time - 10*0.4*abs(self.env.getLegAngle())

    def _isDone(self):
        #  The criteria for finish will be either
        #   - Time "The time is more than t_max
        #   - Fall "The angle is more than theta_max"
        time = self.env.getTime()
        # if time > self.max_time or abs(self.env.getLegAngle()) > np.pi/4:
        if abs(self.env.getLegAngle()) > np.pi/12:
            return True
        return False

    def reset(self):
        # Reset the state of the environment to an initial state, and the self vars to the initial values
        # Reset the environment and the simulator
        self.env.reset()
        self.env.step()
        # Not necessary as long as we didn't comment it in the _takeAction above
        # for i in self.env.controllers_num:
        #     self.env.actions_json["Controllers_val"][i] = 0

        # get the observations after the resetting of the environment
        return self._getObservation()

    def render(self, mode='human'):
        self.env.render()

    def close(self):
        self.env.closeSimulator()