"""leg_env.py: Create the gym custom environment of tensegrity leg"""
__author__ = "Hany Hamed"
__credits__ = ["Hany Hamed", "Prof. Sergie Savin"]
__version__ = "1.0.0"
__email__ = "h.hamed.elanwar@gmail.com / h.hamed@innopolis.university"
__status__ = "Testing"

# ----------------------------------------------------------------------------------------
# Problems that undetermined: [TODO]
# 1). A small action (dl=0.1) give multiple sequence of observation.
#       - [Done] Solution 1: Give the last observation.        [The implemented one]
#       - Solution 2: Give all the sequence of observation.
# 2). Action space is too big and we need to reforumlate it.    
#       - [Done] Solution  : Descirbed in the comments above the corressponding part.
# 3). Should we add got stuck for reward and observation or not????
# 4). close and reset not working properly, they destroy the port number
#       - Make text file with the place of the app of the simulator that every time, both of them read the number and simulator increase the number and this is the number of the port
# 5). We need to remove the upper rods in the holding box as they resist the rods sometimes
#       we will need to change any number of 19 in the whole system
# 6). Add some colors to the model of the world in the simulator
# 7). TODO easy: add stuck flag to the sent json from the simulator
# 8). easy TODO: change the unmodifable "immutable" objects to tuple instead of list because of the concept.
#
# 9). [Done] should be easy TODO [Done] I had to write here the LegModel as it is not installed and copied with the LegEnv
# 10). [Done] change the name of the gym to gym-tensegrity and gym_tensegrity but the env is leg as it is
# 11). TODO [Done]: Change the testing functions to the new action_space and observation_space modifications
# 12). TODO [Done]: Implement new observation_space that will work with stable_baselines
# 13). TODO :add the enabled actuators
# ----------------------------------------------------------------------------------------




# This file will contain all the information about the agent and the environment starting from the rendering of the GUI to the rewards,... etc.
import os
import time
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import sys
import scipy.spatial as ss
import signal
from math import floor,log2

import logging

# logger = logging.getLogger(__name__)

import numpy as np
import math
from gym_tensegrity.envs.leg_model import LegModel

sim_exec = '/home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/src/dev/legz/python_communication_test/helper.sh'


class LegEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, host_name='localhost', port_num=10037, sim_exec=sim_exec,  dl=0.1):
        super(LegEnv, self).__init__()
        # Agent self variables
        self.goal = self._generateGoal()
        self.max_time = 200
        self.max_cable_length = 100
        self.min_coordinate_point = -500
        self.max_coordinate_point = 500
        self.dl = dl
        self.initial_volume = 12464.22707673338 # By testing
        self.collapsed_volume = 10500
        # self.enabled_actuators_list = [] # TODO: for now it will take the first (enabled_actuators_num) as enabled
        # self.enabled_actuators_num =  10   # TODO: in future it will be the length of the list


        # Initial configuration for the leg
        # TODO [Done]:
        #   -setup the leg; initialization, communication, start, and set the variables
        #   -Set the initial goal
        # Creation of the environment and pass the initial configuration
        # TODO: [Done]
        self.env = LegModel(host_name=host_name, port_num=port_num, sim_exec=sim_exec, dl=dl)
        self.env.startSimulator()

        # Example: self.env = Viewer(goal=self.goal)

        # Put the details of the action and observation spaces
        # TODO: [Done]
        #   - action_space  [Done]
        #   - observation_space [Done]
        # Solution 1 for action_space: put the dimension for all permutation that can be happen
        # n_actions = 3**60  #180 #TODO [Done]: this is not the correct action_space, it should be 3^60 to get all the possible combination for the cables trit; for each controller (bit but has 3 values)
        # n_actions = 2**(1+self.env.controllers_num)
        # n_actions = 2**(1+self.enabled_actuators_num)
        # self.action_space = spaces.Discrete(n_actions)  # 180 discrete actions = 3 (+/0/-) for each actuator (60)
        n_actions = 2**(floor(log2(self.env.controllers_num))+1)     # bits that represent the binary number for the index of the controller and an extra bit for the action 0 = decrease, 1 = increase
        self.action_space = spaces.Discrete(n_actions)
        #  Solution 2 for action_space:
        # self.action_space = spaces.MultiDiscrete([3 for i in range(self.env.controllers_num)])
        # TODO: Take into consideration the static cables and rods that are made to make the structure rigid
        #           they should be exculeded from the construction
        # Observations:
        #   - The dimensions is specified above and their min. and max. values
        #   1- Time
        #   2- Cables' lengths
        #   3- Endpoints of rods (include the end_effector)
        # self.observation_space = spaces.Tuple((
        #                         spaces.Box(low=0, high=self.max_time, shape=(1,), dtype=np.float16),
        #                         spaces.Box(low=0, high=self.max_cable_length, shape=(self.env.controllers_num,), dtype=np.float16),
        #                         spaces.Box(low=self.min_coordinate_point, high=self.max_coordinate_point, shape=(self.env.rods_num,3), dtype=np.float16)))
        # self.observation_space = spaces.Box(0, self.max_time, dtype=np.float32)

        low = np.array([0])
        low = np.append(low, np.zeros(self.env.controllers_num))
        low = np.append(low, np.full((1,self.env.rods_num*3*2), self.min_coordinate_point))

        high = np.array([self.max_time])
        high = np.append(high, np.full((1,self.env.controllers_num), self.max_cable_length))
        high = np.append(high, np.full((1,self.env.rods_num*3*2), self.max_coordinate_point))
 
        self.observation_space = spaces.Box(low= low, high= high, dtype=np.float32)
        
        # wrong as we have array of array in the end points(array) and cable lengths, it will need modification
        # low = np.array([
        #     0,
        #     0,
        #     self.min_coordinate_point])
        
        # high = np.array([
        #     self.max_time,
        #     self.max_cable_length,
        #     self.max_coordinate_point])

        # self.observation_space = spaces.Box(low, high, dtype=np.float32)

    def __del__(self):
        self.env.closeSimulator()
            
    # TODO: for now it is static goal
    #           for next is to implement a random goal and validate that it is reachable and in the working space of the end_effector
    # TODO [Done]: add a reachable static goal
    def _generateGoal(self):
        # return (4.252820907910812, 11.42265959555328, -3.1326669704587604)  # Reachable point by the cms of the end-effector rod when the 2nd controller is decreased to 17.1468
        # return (-4.071894028029348, 30.865273129264445, 14.268032968387198)
        return (-4.90788472695319, 30.659340405658163, 20.34403515302529)   # Reachable point by the cms of the end-effector rod when the 2nd controller is increased by 50*dl

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
        # TODO [Done]: change the controller simulator to read and take the action then write the data of the observations
        #           reverse the order of TCP to read the observation of the corresponding action not the previouse one
        self._takeAction(action)
        observation = self._getObservation()
        reward = self._getReward(observation)
        done = self._isDone()
        return observation, reward, done, {}

    # Actions [0,180):
    #   - 3 possible actions for each controller
    #   0+(3*index) -> -1 -> decrease by dl
    #   1+(3*index) ->  0 -> stay the same
    #   2+(3*index) -> +1 -> increase by dl
    def _takeAction(self, action):
        # pass  
        # # Solution 2: Working but not with stable_baseline 
        # # [Feature not implemented yet in their library to have tuple of actions in the action space]
        # # More details about their problem: https://github.com/hill-a/stable-baselines/issues/133
        # # TODO [Done]: put the scheme of the actions for the leg [Done]
        # # TODO [Done]: test !!!
        # # TODO [Done]: chage it according to the new scheme
        # for i in range(self.env.controllers_num):
        #     value = (action[i]-1)*self.dl
        #     self.env.actions_json["Controllers_val"][i] = value
        
        # # if it was zero means that it will be decreased by dl, if it was 1 will be the same, if it was 2 it will be increased
        # self.env.step()
        # # TODO [Done]: wait until the done_flag is set [Done from the side of the simulator]
        
        # Solution 1: Under testing
        # MSB - LSB
        # Each controller has 2 bits:
        #   if the bits 00 = 0 it will mean decrease by dl
        #   if the bits 01 = 1 it will mean stay the same
        #   if the bits 10 = 2 it will mean increase by dl
        #   if the bits 11 = 3 it will mean increase by dl  ? Redundacy in the actions (wasting) Will it make problems in the learning process?
        # for i in range(0, 2*self.env.controllers_num, 2):
        #     value = (1 if (2**i & action) > 0 else 0) + (2 if (2**(i+1) & action) > 0 else 0)
        #     value = min(value, 2) - 1
        #     self.env.actions_json["Controllers_val"][i] = value**self.dl
        # for i in range(self.enabled_actuators_num//2):
        #     box_start_index = i*2
        #     value = (1 if (2**box_start_index & action) > 0 else 0) + (2 if (2**(box_start_index+1) & action) > 0 else 0) + (4 if (2**(box_start_index+2) & action) > 0 else 0)
        #     # print(value, box_start_index)
        #     if (value == 0):
        #         self.env.actions_json["Controllers_val"][box_start_index] = 1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = 0
        #     elif (value == 1):
        #         self.env.actions_json["Controllers_val"][box_start_index] = -1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = 0
        #     elif (value == 2):
        #         self.env.actions_json["Controllers_val"][box_start_index] = 0
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = 1
        #     elif (value == 3):
        #         self.env.actions_json["Controllers_val"][box_start_index] = 1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = 1
        #     elif (value == 4):
        #         self.env.actions_json["Controllers_val"][box_start_index] = -1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = 1
        #     elif (value == 5):
        #         self.env.actions_json["Controllers_val"][box_start_index] = 0
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = -1
        #     elif (value == 6):
        #         self.env.actions_json["Controllers_val"][box_start_index] = 1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = -1
        #     elif (value == 7):
        #         self.env.actions_json["Controllers_val"][box_start_index] = -1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = -1
        #     self.env.actions_json["Controllers_val"][box_start_index] *= self.dl
        #     self.env.actions_json["Controllers_val"][box_start_index+1] *= self.dl
        # self.env.step()
        bits_num = floor(log2(self.env.controllers_num))+1
        value_sign = (1 if ((2**bits_num) & action) > 0 else -1)    # if sign_bit is 0 = decrease, 1 = increase
        value = value_sign*self.dl
        # print(self.env.controllers_num)
        controller_index = min(self.env.controllers_num-1, action - (2**bits_num if value_sign == 1 else 0))
        # TODO: Don't know if it is necessary or not. Maybe here we can set all the controllers to zero and delete the last line in the method
        # print("Controllers_index {:} :::{:}, Controller_value: {:}".format(controller_index, action, value))
        
        self.env.actions_json["Controllers_val"][controller_index] = value
        self.env.step()
        self.env.actions_json["Controllers_val"][controller_index] = 0
        

    # Observations:
    #   - The dimensions is specified above and their min. and max. values
    #   1- Time
    #   2- Cables' lengths
    #   3- Endpoints of rods (include the end_effector)
    # TODO [Done]: conform the return with the new boundries shapes
    def _getObservation(self):
        # TODO[Done]: add the time passed in the observation as it can be used to calculate the reward
        # print(self.env.getTime())
        observation = np.array(self.env.getTime())
        observation = np.append(observation, self.env.getCablesLengths())
        end_points = self.env.getEndPoints()
        end_points_flatten = []
        # print("--------------")
        # print(end_points)
        for end_point_2 in end_points:
            for end_point in end_point_2:
                for pos in end_point:
                    end_points_flatten.append(pos)

        observation = np.append(observation, end_points_flatten)
        # observation = [self.env.getTime(), self.env.getCablesLengths(), self.env.getEndPoints()]
        return np.array(observation)

    def _getReward(self, observation):
        # TODO [Done]:Set the reward criteria, which will depend on:
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
        # TODO [Done]:
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

        eps = 0.1
        distance = self._getDistancetoGoal()
        
        # TODO [Done]: Implement either if it collapsed criteria
        collapsed = self._isCollapsed(self.env.getEndPoints())
        print("Distance between the goal: {:}".format(distance))
        # print("Collapsed: ???: {:}".format(collapsed))
        if(distance <= eps or collapsed == True):
            return True
        return False

    def _getDistancetoGoal(self):
        end_effector = self.env.getEndEffector()
        MSE = 0
        for i in range(3):
            MSE += (end_effector[i] - self.goal[i])**2 
        distance = math.sqrt(MSE)
        return distance

    # TODO [Done]: Implement it
    # By calculating the volume and comparing with the volume that it is known when it collapsed
    #   or under specific threshold
    def _isCollapsed(self, points_raw):
        points = []
        for i in range(len(points_raw)):
            points.append(points_raw[i][0])
            points.append(points_raw[i][1])

        hull = ss.ConvexHull(points)
        # print("Volume: {:}".format(hull.volume))
        # Initial Volume by testing: 12464.22707673338
        eps = 500
        if(hull.volume - self.collapsed_volume <= eps):
            return True
        return False
    
    # TODO [Done]: Problem mentioned in the header
    def reset(self):
        # TODO [Done]:
        # Reset the state of the environment to an initial state, and the self vars to the initial values
        self.goal = self._generateGoal()
        # Reset the environment and the simulator
        self.env.reset()
        # get the observations after the resetting of the environment
        return self._getObservation()

    def render(self, mode='human'):
        # TODO:
        # Example:
        self.env.render()

    # TODO [Done]: Problem mentioned in the header
    def close(self):
        self.env.closeSimulator()
        # sys.exit(0)


# This function for testing the env by itsel
def main():
    def print_observation(obs):
        # Old
        # print("@@@@@@@@@@@\nTime: {:}\n Cables' lengths: {:}\n End points: {:}\n@@@@@@@@@@@".format(obs[0], obs[1], obs[2]))
        print("Observations {:}".format(obs))

        # logging.info("\nTime: {:}\n Cables' lengths: {:}\n End points: {:}\n".format(obs[0], obs[1], obs[2]))
    env = LegEnv()
    # action_arr = np.zeros((2**(2*env.env.controllers_num)))
    # Old
    # action_arr = [1 for _ in range(env.env.controllers_num)]
    # action_arr[2] = 0
    # action_arr[5] = 0

    # init_obs ,_,_,_=env.step(action_arr)
    # print(init_obs[1][2])
    # print(env.env.actions_json)
    # print("")
    # input("-> check point: WAIT for INPUT !!!!")
    # action_arr[2] = 0
    # for _ in range(50):
    #     observation, reward, done, _= env.step(action_arr)
    #     print_observation(observation)
    #     print("Done:???:{:}".format(done))
    # env.reset()
    # time.sleep(5)
    # env.close()
    # # print("")
    input("-> check point: WAIT for INPUT !!!!")
    for i in range(100000):
        action = env.action_space.sample()
        # action = action_arr
        print("--------------- ({:}) ---------------".format(i))
        # logging.debug("--------------- ({:}) ---------------".format(i))
        print("######\nAction: {:}\n######".format(action))
        # logging.info("\nAction: {:}\n".format(action))
        observation, reward, done, _= env.step(action)
        print_observation(observation)
        # if(observation[0] > env.max_time):
        #     break

    # action_arr = [1 for _ in range(env.env.controllers_num)]
    # final_obs ,_,_,_=env.step(action_arr)
    # print(final_obs[1][2])
    # print(env.env.actions_json)
    # print(env.env.sim_json)
    input("-> check point: WAIT for INPUT !!!!")
    # while(1):
    #     observation, reward, done, _= env.step(action_arr)
    #     print_observation(observation)
    #     # print(env.env.getEndEffector())
    #     print("Done:???:{:}".format(done))

        # print("while",observation[1][2])

# Done: it is now working perfectly
def reset_test():
    env = LegEnv()
    action_arr = [1 for _ in range(env.env.controllers_num)]
    for i in range(10):
        init_obs ,_,_,_=env.step(action_arr)
        print(env.reset())
    print("Finished the loop of reseting")
    env.close()
    print("After closing the environment")
    # print(env.reset())
    # init_obs ,_,_,_=env.step(action_arr)
    # env.close()
    # print("Reached the end without any errors")

def learn_test():
    from stable_baselines.common.vec_env import DummyVecEnv
    from stable_baselines.deepq.policies import MlpPolicy
    from stable_baselines import DQN
    def print_observation(obs):
        print("@@@@@@@@@@@\nTime: {:}\n Cables' lengths: {:}\n End points: {:}\n@@@@@@@@@@@".format(obs[0], obs[1], obs[2]))
    env = LegEnv()


def main_new():
    def print_observation(obs):
        print("Observations {:}".format(obs))
    env = LegEnv()
    action = 5+64
    init_obs ,_,_,_=env.step(action)
    print(env.env.actions_json)
    # print("")
    input("-> check point: WAIT for INPUT !!!!")
    for _ in range(50):
        observation, reward, done, _= env.step(action)
        print_observation(observation)
        print("Done:???:{:}".format(done))
    print(env.env.getEndEffector())
    # env.reset()
    # time.sleep(5)
    # env.close()
    # # print("")
    input("-> check point: WAIT for INPUT !!!!")
    for i in range(1000):
        action = env.action_space.sample()
        print("--------------- ({:}) ---------------".format(i))
        print("######\nAction: {:}\n######".format(action))
        observation, reward, done, _= env.step(action)
        print_observation(observation)
        # if(observation[0] > env.max_time):
        #     break
    action = 0
    final_obs ,_,_,_=env.step(action)
    print(env.env.actions_json)
    print(env.env.sim_json)
    input("-> check point: WAIT for INPUT !!!!")
    while(1):
        observation, reward, done, _= env.step(action)
        print_observation(observation)
        # print(env.env.getEndEffector())
        print("Done:???:{:}".format(done))

if __name__ == "__main__":
    main_new()
    # reset_test()
