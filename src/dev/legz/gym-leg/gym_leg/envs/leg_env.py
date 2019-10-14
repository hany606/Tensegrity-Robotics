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
        self.num_hits = 0
        self.max_num_hit = 5
        # Initial configuration for the leg
        # TODO:
        #   -set the initial configuration for the drone
        #   -Set the initial goal
        # Creation of the drone racer and pass the initial configuration
        # TODO: [Done]
        self.env = LegModel()
        self.env.startSimulator()

        # Example: self.env = Viewer(goal=self.goal)

        # Put the details of the action and observation spaces
        # TODO:
        #   - action_dim
        #   - action_space  [Done]
        #   - observation_space
        # self.action_dim = 2
        self.action_space = spaces.Discrete(120)  # 120 discrete actions = 2 (+/-) for each actuator (60)
        self.observation_space = spaces.Box(
            low=np.array([0, 0]), high=np.array([400, 400]), dtype=np.float16)

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
        self._take_action(action)
        observation = self._get_observation()
        reward = self._get_reward(observation)
        done = self._is_done()
        return observation, reward, done, {}

    def _take_action(self, action):
        # TODO: put the scheme of the actions for the drone [Done]
        if action == 0:
            self.env.z_rotate_CCW()
        elif action == 1:
            self.env.z_rotate_CW()
        elif action == 2:
            self.env.x_rotate_CCW()
        elif action == 3:
            self.env.x_rotate_CW()
        elif action == 4:
            self.env.y_rotate_CCW()
        elif action == 5:
            self.env.y_rotate_CW()
        elif action == 6:
            self.env.z_down()
        elif action == 7:
            self.env.z_up()
        elif action == 8:
            self.env.x_right()
        elif action == 9:
            self.env.x_left()
        elif action == 10:
            self.env.y_forward()
        elif action == 11:
            self.env.y_backward()

        self.env.move()

    def _get_observation(self):
        current_stat = self.env.get_state()
        # TODO: add the time passed in the observation as it can be used to calculate the reward
        observation = [self.env.get_orientation(state=current_stat), self.env.get_position(state=current_stat)
            , self.env.get_angular_acceleration(state=current_stat), self.env.get_angular_velocity(state=current_stat)
            , self.env.get_linear_acceleration(state=current_stat), self.env.get_linear_velocity(state=current_stat)]
        return observation

    def _get_reward(self, observation):
        # TODO:Set the reward criteria, which will be the difference between the distance between the point and the current position
        # Example:
        # end_effector = self.env.get_end_effector()
        # distance = math.sqrt((end_effector[0] - self.goal['x']) ** 2 + (end_effector[1] - self.goal['y']) ** 2)
        # print(distance)
        # if not(self.env.get_end_effector()[0] == self.goal['x'] and self.env.get_end_effector()[1] == self.goal['y']):
        # eps = 60
        # if distance < eps:
        #     return 100
        # return -max(int(distance / 100), 1)
        return -1

    def _is_done(self):
        # TODO:
        #  The criteria for finish will be either
        #       - it hits anything more than a specific threshold
        #       - Reached the goal or near to it

        # Example:
        # end_effector = self.env.get_end_effector()
        # distance = math.sqrt((end_effector[0] - self.goal['x']) ** 2 + (end_effector[1] - self.goal['y']) ** 2)
        # # if not(self.env.get_end_effector()[0] == self.goal['x'] and self.env.get_end_effector()[1] == self.goal['y']):
        # eps = 60
        # if distance < eps:
        #     return 1

        eps = 60
        distance = 0    # TODO
        if self.num_hits > self.max_num_hit or distance < eps:
            return 1
        return 0

    def reset(self):
        # TODO:
        # Reset the state of the environment to an initial state, and the self vars to the initial values
        self.num_hits = 0
        # Reset the environments
        self.env.reset()
        # get the observations after the resetting of the environment
        return self._get_observation()

    def render(self, mode='human'):
        # TODO:
        # Example:
        self.env.render()

    def close(self):
        self.env.close()
