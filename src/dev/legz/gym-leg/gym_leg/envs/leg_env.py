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
# 9). should be easy TODO I had to write here the LegModel as it is not installed and copied with the LegEnv
# 10). change the name of the gym to gym-tensegrity and gym_tensegrity but the env is leg as it is
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

import logging

# logger = logging.getLogger(__name__)

import numpy as np
import math
# from leg_model import LegModel

"""leg_model.py: Create the agent of model of the leg and provide an easy interface to be used with RL algorithms"""
__author__ = "Hany Hamed"
__credits__ = ["Hany Hamed", "Prof. Sergie Savin"]
__version__ = "0.0.1"
__email__ = "h.hamed.elanwar@gmail.com / h.hamed@innopolis.university"
__status__ = "Production"


import socket
import sys
import signal
import json
from time import *
import os
import subprocess
import random
import numpy as np
from transforms3d.euler import euler2mat

sim_exec = '/home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/src/dev/legz/python_communication_test/helper.sh'

class LegModel():
    def __init__(self, host_name='localhost', port_num=10037, packet_size=5000,
                 sim_exec=sim_exec, dl=0.1, rods_num=19, controllers_num=60,
                 end_effector_index=4):
        self.host_name = host_name
        self.port_num = port_num
        self.packet_size = packet_size
        self.sim_exec = sim_exec
        self.actions_json = {
            'Controllers_val': [0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0],
            'Reset': 0
        }
        self.sim_json = {"Flags":[1,0,0]}
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
        # self.sock = socket.socket(socket.SOL_SOCKET, socket.SO_REUSEADDR)    # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(self.port_num)
        self.server_address = (self.host_name, self.port_num) # Bind the socket to the port

        self.connection = None
        self.client_address = None
        self.child_process = None
        print('#########\nstarting up on {} port {}\n#########'.format(self.server_address, self.port_num))
        # print(self.server_address)
        self.sock.bind(self.server_address)
        self.sock.listen(1)  # Listen for incoming connections
        self.reset_flag = False
        self.close_flag = False
        self.dl = dl                            # Self modified parameter
        self.rods_num = rods_num                  # Self modified parameter
        self.controllers_num = controllers_num    # Self modified parameter
        self.end_effector_index = end_effector_index    # Self modified parameter

    def __del__(self):
        self.closeSimulator()
        # sys.exit(0)

    # function for writing data into TCP connection
    def write(self, data):
        # print('sending data to the client:"{}"'.format(data))
        try:
            self.connection.sendall(data.encode())
        except Exception as e:
            print("$$$$$$$$$$$$ ERROR in Writing $$$$$$$$$$$$")
            print("Error: " + str(e))

    # function for reading data from TCP connection
    def read(self):
        try:
            data = []
            counter = 1
            # Receive the data in small chunks and retransmit it
            while True:
                data.append(self.connection.recv(self.packet_size).decode("utf-8"))         #reading part
                # print('{} received "{}"'.format(counter,data[-1]))
                # print(data[-1][-14:-1], ('ZFinished' in str(data[-1][-14:-1])))
                if 'ZFinished' in str(data[-1][-14:-1]):
                    # print("FINISHED*************")
                    # sleep(5)
                    break
                counter += 1
            return "".join(data)
        except ValueError:
            print(ValueError)
            print("$$$$$$$$$$$$ ERROR in Reading $$$$$$$$$$$$")
            # sleep(2)
            return None

    def startSimulator(self):
        self.close_flag = False
        self.reset_flag = False
        if(self.sim_exec == sim_exec):
            print("#Warning: Starting an old version")
        # sleep(0.5)
        self.child_process = subprocess.Popen(self.sim_exec)
        print('#########\nwaiting for a connection\n#########')
        self.connection, self.clientAddress = self.sock.accept()  #wait until it get a client
        print('connection from', self.clientAddress)

    def closeSimulator(self):
        self.close_flag = True
        # kill the shell script of the simulator
        if self.connection is not None:
            self.connection.close()
        if self.child_process is not None:
            os.kill(self.child_process.pid, signal.SIGKILL)

    def render(self):
        pass
    
    def reset(self):
        self.reset_flag = True
        self.closeSimulator()
        # os.kill(self.child_process.pid, signal.SIGTERM)
        # sleep(1)
        self.startSimulator()

    # TODO: make a general step function
    def step(self):
        if (self.close_flag == False):
            if (self.reset_flag == True):
                self.reset()
            
            # if(self.sim_json["Flags"][0] == 1):
            #     self.actions_json["Controllers_val"][2] = -1*self.actions_json["Controllers_val"][2]
            #     self.actions_json["Controllers_val"][5] = -1*self.actions_json["Controllers_val"][5]
                
                # print("FLIP")
                # input()            
            # print("write")
            self.write(json.dumps(self.actions_json))   # Write to the simulator module the json object with the required info

            sim_raw_data = self.read()
            # print(sim_raw_data)
            if(sim_raw_data is not None):
                self.sim_json = json.loads(sim_raw_data)  # Parse the data from string to json
            # print(self.sim_json["Center_of_Mass"][4])
            # print("step Function",self.sim_json["Cables_lengths"][2])

        else:
            self.closeSimulator()

    def getCablesLengths(self, i=None):
        # print("getCableLengths Function",self.sim_json["Cables_lengths"][2])
        if(i is None):
            return self.sim_json["Cables_lengths"]
        return self.sim_json["Cables_lengths"][i]
        
    #TODO
    def _getEndPointsByRod(self, rod_num):
        # print(self.sim_json["Center_of_Mass"][0])
        # print(rod_num, type(rod_num))
        # rods_cms = self.sim_json["Center_of_Mass"][rod_num]
        # rods_orientation = self.sim_json["Orientation"][rod_num]
        # print("Orientation", rods_orientation)
        # Coordinates_in_rod_sys = Rotation_matrix*Coordinates_in_global_sys + CMS
        # (Coordinates_in_rod_sys - CMS)*inv(Rotation_matrix) = Coordinates_in_global_sys
        # ....
        # ....
        # ....
        # [endPoint1, endPoint2] -> [x,y,z]
        # return [[rods_cms[0],rods_cms[1],rods_cms[2]], [rods_cms[0],rods_cms[1],rods_cms[2]]]       #TODO change this
        end_point1 = self.sim_json["End_points"][rod_num][0]
        end_point2 = self.sim_json["End_points"][rod_num][1]
        return [[end_point1[0],end_point1[1],end_point1[2]], [end_point2[0],end_point2[1],end_point2[2]]]
    
    def getEndPoints(self, rod_num=None):
        if(rod_num is None):
            # [rod1, rod2,...] -> [endPoint1, endPoint2] -> [x,y,z]
            end_points = []
            for i in range(self.rods_num):
                end_points.append(self._getEndPointsByRod(i))
            return end_points
        return self._getEndPointsByRod(rod_num)

    def getEndEffector(self):
        return self._getEndPointsByRod(self.end_effector_index)[1]

        
    
    def getTime(self):
        print(self.sim_json)
        return self.sim_json["Time"]


sim_exec = '/home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/src/dev/legz/python_communication_test/helper.sh'


class LegEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, host_name='localhost', port_num=10036, sim_exec=sim_exec,  dl=0.1):
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


        # Initial configuration for the leg
        # TODO: [Done]
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
        # self.action_space = spaces.Discrete(n_actions)  # 180 discrete actions = 3 (+/0/-) for each actuator (60)
        # Solution 2 for action_space:
        self.action_space = spaces.MultiDiscrete([3 for i in range(self.env.controllers_num)])
        # TODO: Take into consideration the static cables and rods that are made to make the structure rigid
        #           they should be exculeded from the construction
        # Observations:
        #   - The dimensions is specified above and their min. and max. values
        #   1- Time
        #   2- Cables' lengths
        #   3- Endpoints of rods (include the end_effector)
        self.observation_space = spaces.Tuple((
                                spaces.Box(low=0, high=self.max_time, shape=(1,), dtype=np.float16),
                                spaces.Box(low=0, high=self.max_cable_length, shape=(self.env.controllers_num,), dtype=np.float16),
                                spaces.Box(low=self.min_coordinate_point, high=self.max_coordinate_point, shape=(self.env.rods_num,3), dtype=np.float16)))

    def __del__(self):
        self.env.closeSimulator()
            
    # TODO: for now it is static goal
    #           for next is to implement a random goal and validate that it is reachable and in the working space of the end_effector
    # TODO [Done]: add a reachable static goal
    def _generateGoal(self):
        # return (4.252820907910812, 11.42265959555328, -3.1326669704587604)  # Reachable point by the cms of the end-effector rod when the 2nd controller is decreased to 17.1468
        return (-4.071894028029348, 30.865273129264445, 14.268032968387198)

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
        # TODO[Done]: change the controller simulator to read and take the action then write the data of the observations
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
        # TODO [Done]: put the scheme of the actions for the leg [Done]
        # TODO [Done]: test !!!
        # TODO [Done]: chage it according to the new scheme
        for i in range(self.env.controllers_num):
            value = (action[i]-1)*self.dl
            self.env.actions_json["Controllers_val"][i] = value
        
        # if it was zero means that it will be decreased by dl, if it was 1 will be the same, if it was 2 it will be increased
        self.env.step()
        # TODO: wait until the done_flag is set [Done from the side of the simulator]

    # Observations:
    #   - The dimensions is specified above and their min. and max. values
    #   1- Time
    #   2- Cables' lengths
    #   3- Endpoints of rods (include the end_effector)
    # TODO: conform the return with the new boundries shapes
    def _getObservation(self):
        # TODO: add the time passed in the observation as it can be used to calculate the reward
        observation = (self.env.getTime(), self.env.getCablesLengths(), self.env.getEndPoints())
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
        print("Collapsed: ???: {:}".format(collapsed))
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

    # TODO[Done]: Implement it
    # By calculating the volume and comparing with the volume that it is known when it collapsed
    #   or under specific threshold
    def _isCollapsed(self, points_raw):
        points = []
        for i in range(len(points_raw)):
            points.append(points_raw[i][0])
            points.append(points_raw[i][1])

        hull = ss.ConvexHull(points)
        print("Volume: {:}".format(hull.volume))
        # Initial Volume by testing: 12464.22707673338
        eps = 500
        if(hull.volume - self.collapsed_volume <= eps):
            return True
        return False
    
    # TODO[Done]: Problem mentioned in the header
    def reset(self):
        # TODO:
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

    # TODO[Done]: Problem mentioned in the header
    def close(self):
        self.env.closeSimulator()
        # sys.exit(0)


# This function for testing the env by itsel
def main():
    def print_observation(obs):
        print("@@@@@@@@@@@\nTime: {:}\n Cables' lengths: {:}\n End points: {:}\n@@@@@@@@@@@".format(obs[0], obs[1], obs[2]))
        # logging.info("\nTime: {:}\n Cables' lengths: {:}\n End points: {:}\n".format(obs[0], obs[1], obs[2]))
    env = LegEnv()
    action_arr = [1 for _ in range(env.env.controllers_num)]
    # action_arr[2] = 0
    # action_arr[5] = 0

    init_obs ,_,_,_=env.step(action_arr)
    print(init_obs[1][2])
    print(env.env.actions_json)
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
    # input("-> check point: WAIT for INPUT !!!!")
    # for i in range(100000):
    #     action = env.action_space.sample()
    #     # action = action_arr
    #     print("--------------- ({:}) ---------------".format(i))
    #     # logging.debug("--------------- ({:}) ---------------".format(i))
    #     print("######\nAction: {:}\n######".format(action))
    #     # logging.info("\nAction: {:}\n".format(action))
    #     observation, reward, done, _= env.step(action)
    #     print_observation(observation)
    #     # if(observation[0] > env.max_time):
    #     #     break

    action_arr = [1 for _ in range(env.env.controllers_num)]
    # final_obs ,_,_,_=env.step(action_arr)
    # print(final_obs[1][2])
    # print(env.env.actions_json)
    # print(env.env.sim_json)
    # input("-> check point: WAIT for INPUT !!!!")
    while(1):
        observation, reward, done, _= env.step(action_arr)
        print_observation(observation)
        # print(env.env.getEndEffector())
        print("Done:???:{:}".format(done))

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


if __name__ == "__main__":
    # main()
    reset_test()
