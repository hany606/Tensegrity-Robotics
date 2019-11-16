"""jumper_env.py: Create the gym custom environment of tensegrity one legged jumpeing robot"""
__author__ = "Hany Hamed"
__credits__ = ["Hany Hamed", "Prof. Sergie Savin"]
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

# logger = logging.getLogger(__name__)

import numpy as np
import math
from gym_tensegrity.envs.jumper_model import JumperModel

sim_exec = '/home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/src/dev/jumper/util/helper.sh'


class JumperEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, host_name='localhost', port_num=10040, sim_exec=sim_exec,  dl=0.1):
        super(JumperEnv, self).__init__()
        # Agent self variables
        self.max_time = 200
        self.max_cable_length = 100
        self.min_leg_angle = -np.pi/2
        self.max_leg_angle =  np.pi/2
        self.dl = dl
        
        self.env = JumperModel(host_name=host_name, port_num=port_num, sim_exec=sim_exec, dl=dl)
        self.env.startSimulator()

        n_actions = 2**(floor(log2(self.env.controllers_num))+1)
        self.action_space = spaces.Discrete(n_actions)
        
        low = np.array(self.min_leg_angle)
        low = np.append(low, np.zeros(self.env.controllers_num))

        high = np.array(self.max_leg_angle)
        high = np.append(high, np.full((1,self.env.controllers_num), self.max_cable_length))
 
        self.observation_space = spaces.Box(low= low, high= high, dtype=np.float32)

    def __del__(self):
        self.env.closeSimulator()
            
    def step(self, action):
        """
        Parameters
        ----------
        action :

        Returns
        -------
        observation, reward, episode_over(done), info : tuple
            observation (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            done (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        # TODO [Done]: change the controller simulator to read and take the action then write the data of the observations
        #           reverse the order of TCP to read the observation of the corresponding action not the previouse one
        self._takeAction(action)
        observation = self._getObservation()
        reward = self._getReward(observation)
        done = self._isDone()
        return observation, reward, done, {}

    # 3 bits for the index of the cable, 1 bit (the last one) for the direction of the controller (increase or decrease)
    def _takeAction(self, action):
        bits_num = floor(log2(self.env.controllers_num))+1
        value_sign = (1 if ((2**bits_num) & action) > 0 else -1)    # if sign_bit is 0 = decrease, 1 = increase
        value = value_sign*self.dl
        # print(self.env.controllers_num)
        controller_index = action - (2**(bits_num-1) if value_sign == 1 else 0)
        print("Controllers_index {:} :::{:}, Controller_value: {:}".format(controller_index, action, value))
        
        # TODO: Don't know if it is necessary or not. Maybe here we can set all the controllers to zero and delete the last line in the method
        self.env.actions_json["Controllers_val"][controller_index] = value
        self.env.step()
        self.env.actions_json["Controllers_val"][controller_index] = 0    # IF we comment that, this will enable the environment to operate simultanously actuators
        

    # Observations:
    #   - The dimensions is specified above and their min. and max. values
    #   1- Angle of the leg
    #   2- Cables' lengths
    # TODO:
    #   - Check the observation strucutre
    def _getObservation(self):
        observation = np.empty((1,0))
        observation = np.append(observation, self.env.getCablesLengths())

        observation = np.append(observation, self.env.getLegAngle())
        return np.array(observation)

    # TODO
    def _getReward(self, observation):
        # Reward Criteria will depend on:
        #   - The angle of the leg
        #   - The time
        # TODO: Add the time and normalize it
        time = self.env.getTime()
        done_reward = 0
        if self._isDone():
            done_reward = 100
        return time + done_reward

    # TODO
    def _isDone(self):
        # TODO :
        #  The criteria for finish will be either
        #   - Time "The time is more than t_max
        #   - Fall "The angle is more than theta_max"
        return False

    # TODO
    def reset(self):
        # Reset the state of the environment to an initial state, and the self vars to the initial values
        # Reset the environment and the simulator
        self.env.reset()
        # get the observations after the resetting of the environment
        return self._getObservation()

    def render(self, mode='human'):
        # TODO:
        # Example:
        self.env.render()

    def close(self):
        self.env.closeSimulator()
        # sys.exit(0)

def main():
    def print_observation(obs):
        print("Observations {:}".format(obs))


if __name__ == "__main__":
    main()
