# This file will contain all the information about the agent and the environment starting from the rendering of the GUI to the rewards,... etc.
import os
import time
import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding

import logging

logger = logging.getLogger(__name__)

import numpy as np
import math
from leg_model import LegModel


class LegEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Agent self variables
        self.goal = self._generateGoal()
        # Initial configuration for the leg
        # TODO:
        #   -setup the leg; initialization, communication, start, and set the variables
        #   -Set the initial goal
        # Creation of the environment and pass the initial configuration
        # TODO: [Done]
        self.env = LegModel()
        self.env.startSimulator()

        # Example: self.env = Viewer(goal=self.goal)

        # Put the details of the action and observation spaces
        # TODO:
        #   - action_space  [Done]
        #   - observation_space
        self.action_space = spaces.Discrete(180)  # 180 discrete actions = 3 (+/0/-) for each actuator (60)
        # TODO: Take into consideration the static cables and rods that are made to make the structure rigid
        #           they should be exculeded from the construction
        self.observation_space = spaces.Box(
            low=np.array([0, 0]), high=np.array([400, 400]), dtype=np.float16)

    # TODO: for now it is static goal
    #           for next is to implement a random goal and validate that it is reachable and in the working space of the end_effector
    # TODO: add a reachable static goal
    def _generateGoal(self):
        return [0,0,0]

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
            episode_over (bool) :
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
        # TODO: change the controller simulator to read and take the action then write the data of the observations
        #           reverse the order of TCP to read the observation of the corresponding action not the previouse one
        observation = self._getObservation()
        self._takeAction(action)
        reward = self._getReward(observation)
        done = self._isDone()
        return observation, reward, done, {}

    # Actions [0,180):
    #   - 3 possible actions for each controller
    #   0+(3*index) -> -1 -> decrease by dl
    #   1+(3*index) ->  0 -> stay the same
    #   2+(3*index) -> +1 -> increase by dl
    def _takeAction(self, action):
        # TODO: put the scheme of the actions for the leg [Done]
        # TODO: test !!!
        index = action//3
        value = (action%3)-1
        # if it was zero means that it will be decreased by dl, if it was 1 will be the same, if it was 2 it will be increased
        self.env.actions_json[index] = value
        self.env.step()

    # Observations:
    #   - The dimensions is specified above and their min. and max. values
    #   1- Time
    #   2- Cables' lengths
    #   3- Endpoints of rods (include the end_effector)
    def _getObservation(self):
        # TODO: add the time passed in the observation as it can be used to calculate the reward
        observation = [self.env.getTime(), self.env.getCablesLengths(), self.env.getEndPoints()]
        return observation

    def _getReward(self, observation):
        # TODO:Set the reward criteria, which will depend on:
        #   - Euclidian distance between the end-effector and the target_point
        #   - The stability of the structure -> depends on the minimum volume of the structure when collapse
        #   - The time

        # Example:
        # end_effector = self.env.get_end_effector()
        # distance = math.sqrt((end_effector[0] - self.goal['x']) ** 2 + (end_effector[1] - self.goal['y']) ** 2)
        # print(distance)
        # if not(self.env.get_end_effector()[0] == self.goal['x'] and self.env.get_end_effector()[1] == self.goal['y']):
        # eps = 60
        # if distance < eps:
        #     return 100
        # return -max(int(distance / 100), 1)

        return -0.1*self._getDistancetoGoal()-0.01*self.env.getTime()

    def _isDone(self):
        # TODO:
        #  The criteria for finish will be either
        #       - it collapsed or not
        #       - Reached the goal or near to it

        # Example:
        # end_effector = self.env.get_end_effector()
        # distance = math.sqrt((end_effector[0] - self.goal['x']) ** 2 + (end_effector[1] - self.goal['y']) ** 2)
        # # if not(self.env.get_end_effector()[0] == self.goal['x'] and self.env.get_end_effector()[1] == self.goal['y']):
        # eps = 60
        # if distance < eps:
        #     return 1

        eps = 0.01
        distance = self._getDistancetoGoal()
        
        # TODO: Implement either if it collapsed criteria
        collapsed = self._isCollapsed
        if(distance <= eps and collapsed != False):
            return True

        return False
    def _getDistancetoGoal(self):
        end_effector = self.env.getEndEffector()
        MSE = 0
        for i in range(3):
            MSE += (end_effector[i] - self.goal[i])**2 
        distance = math.sqrt(MSE)
        return distance

    # TODO: Implement it
    # By calculating the volume and comparing with the volume that it is known when it collapsed
    #   or under specific threshold
    def _isCollapsed(self):
        return False

    def reset(self):
        # TODO:
        # Reset the state of the environment to an initial state, and the self vars to the initial values

        # Reset the environments
        self.env.reset()
        # get the observations after the resetting of the environment
        return self._getObservation()

    def render(self, mode='human'):
        # TODO:
        # Example:
        self.env.render()

    def close(self):
        self.env.closeSimulator()
