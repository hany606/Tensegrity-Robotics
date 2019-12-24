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
from random import randint

# logger = logging.getLogger(__name__)

import numpy as np
import math
from gym_tensegrity.envs.jumper_model import JumperModel

# Machine with Xscreen
sim_exec = 'gnome-terminal -e /home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/build/dev/jumper/AppJumperModel'
#Headless
# sim_exec = '/home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/build/dev/jumper/AppJumperModel'

class JumperEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, host_name='localhost', port_num=10042, sim_exec=sim_exec,  dl=0.1):
        super(JumperEnv, self).__init__()
        # Agent self variables
        self.max_time = 200
        self.max_cable_length = 50
        self.min_leg_angle = -np.pi/2
        self.max_leg_angle =  np.pi/2
        self.dl = dl
        
        self.env = JumperModel(host_name=host_name, port_num=port_num, sim_exec=sim_exec, dl=dl)
        self.env.startSimulator()

        # 3 bits for indexing the cable's controller 2^3 = 8 and one bit for the control direction
        # This action space will inforce to have only one working controller at a time
        # Also, always one controller work at least there is no possibilty to have all of them not working, to aoid this point we can add another bit fot the control direction 
        
        # Discrete Action space
        # n_actions = 2**(floor(log2(self.env.controllers_num))+1)
        # self.action_space = spaces.Discrete(n_actions)
        
        # Continuous Action space
        low = np.array([0 for i in range(self.env.controllers_num)])
        high = np.array([self.max_cable_length for i in range(self.env.controllers_num)])
        self.action_space = spaces.Box(low=low, high=high, dtype=np.float32)

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

    # Continuous
    # action is vector of continuous values for the controllers of the strings
    def _takeAction(self, action):
        if(isinstance(action, np.ndarray)):
            action_list = action.tolist()
        else:
            action_list = action
        self.env.actions_json["Controllers_val"][:] = action_list
        self.env.step()



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
        # TODO:
        # Example:
        self.env.render()

    def close(self):
        self.env.closeSimulator()
        # sys.exit(0)

# Discrete action space functions testing
def main(port_num=10042):
    def print_observation(obs):
        print("Observations {:}".format(obs))
    env = JumperEnv(port_num=port_num)
    # action = randint(0,15)
    action = 14
    # print("Action: {:}".format(action))
    init_obs ,_,_,_=env.step(action)
    # print_observation(init_obs)
    # print(env.env.actions_json)
    # print("")

    # input("-> check point: WAIT for INPUT !!!!")
    # for i in range(50):
    #     input("-> check point: WAIT for INPUT !!!!")
    #     observation, reward, done, _= env.step(action)
    #     print_observation(observation)
    #     print("Done:???:{:}".format(done))

    # input("-> check point: WAIT for INPUT !!!!")
    # for i in range(1,1001):
    #     action = env.action_space.sample()
    #     # action = 2
    #     input("-> check point: WAIT for INPUT !!!!")
    #     print("--------------- ({:}) ---------------".format(i))
    #     print("######\nAction: {:}\n######".format(action))
    #     observation, reward, done, _= env.step(action)
    #     print_observation(observation)
    #     print("Done:???:{:}".format(done))

    # input("-> check point: WAIT for INPUT !!!!")

    # for i in range(50):
    #     observation, reward, done, _= env.step(2)

    # input("-> check point: WAIT for INPUT !!!!")


    flag = 0
    # i = 0
    while True:
        # i += 1
        # print(i)
        # if(i > 100):
        #     i = 0
        #     env.reset()
        inp = "d"
        # inp = input("~~~~~~input: ")
        if(inp == "w"):
            flag = 1
        elif(inp == "s"):
            flag = -1
        elif(inp == "d"):
            flag = 0

        if(flag <= 0):
            observation, reward, done, _= env.step(4)
            observation, reward, done, _= env.step(5)
        if(flag >= 0):
            observation, reward, done, _= env.step(12)
            observation, reward, done, _= env.step(13)
        print(observation)
        print("angle:{:}".format(observation[-1]*180/np.pi))

def forked_process_main():
    port_num_base = 10042
    num_threads = 2
    for i in range(num_threads):
        pid = os.fork()
        print("fork {:}".format(pid))
        if(pid > 0):
            print("Child: {:} -> on port: {:}".format(pid, port_num_base+i))
            main(port_num_base+i)

def threaded_main():
    import threading
    port_num_base = 10042
    num_threads = 10
    threads_list = []
    for i in range(num_threads):
        threads_list.append(threading.Thread(target=main, args=(port_num_base+i,)))
    
    for i in range(num_threads):
        threads_list[i].start()

# Continuous action space functions testing
def main_cont(port_num=10042):
    def print_observation(obs):
        print("Observations {:}".format(obs))
    env = JumperEnv(port_num=port_num)
    # action = randint(0,15)
    action = [7.95 for i in range(8)]
    # action[0] = 5
    print("Action: {:}".format(action))
    # input("-> check point: WAIT for INPUT !!!!")
    init_obs ,_,_,_=env.step(action)

    print_observation(init_obs)
    # print(env.env.actions_json)
    # print("")

    # input("-> check point: WAIT for INPUT !!!!")

    flag = 0
    # i = 0
    while True:
        observation, reward, done, _= env.step(init_obs[:-1])
        print(observation)
        print("angle:{:}".format(observation[-1]*180/np.pi))

if __name__ == "__main__":
    main_cont()
    # main()
    # forked_process_main()
    # threaded_main()
