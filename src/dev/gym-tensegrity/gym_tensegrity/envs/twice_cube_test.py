import gym
import gym_tensegrity
import numpy as np
import os
from time import sleep

def test(config=None):
    def print_observation(obs):
        # This printing for the default observation
        print("Observations: ")
        for i in range(6):
            print("#{:} Nodes: {:}".format(i+1, [obs[3*i:3*(i+1)]]))
        print("---")
        for i in range(6):
            print("#{:} Nodes velocity: {:}".format(i+1, [obs[3*(i+6):3*(i+1+6)]]))
        print("----------------------------------")
    if(config is not None):
        env = gym.make('gym_tensegrity:twice-cube-v0', config=config)
    if(config is None):
        env = gym.make('gym_tensegrity:twice-cube-v0') 
           
    observation = env.reset()
    print_observation(observation)
    tot_reward = 0
    action = np.array([0. for i in range(8)])
    done = False
    # input("-> check point: WAIT for INPUT !!!!")

    while not done:
        #inp = input("INPUT")
        action = env.action_space.sample()
        action = [0 for i in action]
        action[:4] = [0.001 for i in range(4)]
        action[4:] = [-0.001 for i in range(4)]
        action = np.array(action)
        # print("Action: {:}".format(action))
        observation, reward, done, _= env.step(action)
        print(len(observation))
        tot_reward += reward
        # print("Reward: {:}, Done: {:}".format(reward,done))
        # print(f"MSE: {env._mse_payload()}")
        # print("Time: {:}".format(env.env.getTime()))
        # print_observation(observation)
        # print(env.env.getPayLoad()[0])
        # print("Total Reward: {:}".format(tot_reward))
        # input("-> check point: WAIT for INPUT !!!!")

    #     # sleep(0.01)
    # input("-> check point: WAIT for INPUT !!!!")

    # flag = 0
    # while True:
    #     inp = 'd'
    #     # inp = input("~~~~~~input: ")
    #     #action = env.action_space.sample()
    #     #observation, reward, done, _= env.step(action)

    #     if(inp == "w"):
    #         flag = 1
    #     elif(inp == "s"):
    #         flag = -1
    #     elif(inp == "d"):
    #         flag = 0

    #     if(flag < 0):
    #         action[0] = -0.1
            
    #     if(flag > 0):
    #         action[0] = 0.1

    #     if(flag == 0):
    #         action[0] = 0

    #     observation, reward, done, _= env.step(action)
    #     print(action)
    #     print_observation(observation)


if __name__ == "__main__":
    # test({"goal_coordinate": [-0.09699148, -0.38100061,  0.10062749]})
    # test({"render": True})
    test({'observation': ['nodes', 'nodes_velocities', 'rest_length']})