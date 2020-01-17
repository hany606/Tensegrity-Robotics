import gym
import gym_tensegrity
import numpy as np
import os
from time import sleep

# Discrete action space functions testing
def main(port_num=10042):
    def print_observation(obs):
        print("Observations {:}".format(obs))
    env = gym.make('gym_tensegrity:jumper-v0')
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
            config = {"port_num":port_num_base+i}
            main(config)

def threaded_main():
    import threading
    port_num_base = 10042
    num_threads = 10
    threads_list = []
    for i in range(num_threads):
        config = {"port_num":port_num_base+i}
        threads_list.append(threading.Thread(target=main, args=(config,)))
    
    for i in range(num_threads):
        threads_list[i].start()

# Continuous action space for lengths function testing
def main_cont_lengths(port_num=10042):
    def print_observation(obs):
        print("Observations {:}".format(obs))
    env = gym.make('gym_tensegrity:jumper-v0')
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

# Continuous action space for delta lengths function testing
def main_cont_dlengths(config):
    def print_observation(obs):
        print("Observations {:}".format(obs))
    tot_reward = 0
    env = gym.make('gym_tensegrity:jumper-v0', config=config)
    # action = randint(0,15)
    action = np.array([0. for i in range(8)])
    # action[0] = 1.7
    print("Action: {:}".format(action))
    # input("-> check point: WAIT for INPUT !!!!")
    init_obs ,tot_reward,done,_=env.step(action)

    print_observation(init_obs)
    action[0] = 0
    # print(env.env.actions_json)
    # print("")

    input("-> check point: WAIT for INPUT !!!!")

    while not done:
        action = env.action_space.sample()
        observation, reward, done, _= env.step(action)
        tot_reward += reward
        print("Action: {:}".format(action))

        # input("-> check point: WAIT for INPUT !!!!")
        print("Reward: {:}, Done: {:}".format(reward,done))
        print("Time: {:}".format(env.env.getTime()))
        print_observation(observation)
        print("angle:{:}".format(env.env.getLegAngle()*180/np.pi))
        print("Total Reward: {:}".format(tot_reward))
        # sleep(0.01)
    input("-> check point: WAIT for INPUT !!!!")

    while True:
        inp = "d"
        inp = input("~~~~~~input: ")
        #action = env.action_space.sample()
        #observation, reward, done, _= env.step(action)

        if(inp == "w"):
            flag = 1
        elif(inp == "s"):
            flag = -1
        elif(inp == "d"):
            flag = 0

        if(flag < 0):
            action[0] = -0.1
            observation, reward, done, _= env.step(action)
        #     # action[0] = 0
        #     # observation, reward, done, _= env.step(action)
        if(flag > 0):
            action[0] = 0.1
            observation, reward, done, _= env.step(action)
        #     # action[0] = 0
        #     # observation, reward, done, _= env.step(action)
        if(flag == 0):
            action[0] = 0
            observation, reward, done, _= env.step(action)

        print(observation)
        print("angle:{:}".format(env.env.getLegAngle()*180/np.pi))
    
def test(config=None):
    def print_observation(obs):
        # This printing for the default observation
        print("Observations: ")
        for i in range(6):
            print("#{:} End point: {:}".format(i+1, [obs[3*i:3*(i+1)]]))
        print("---")
        for i in range(6):
            print("#{:} End point velocity: {:}".format(i+1, [obs[3*(i+6):3*(i+1+6)]]))
        print("----------------------------------")
    if(config is not None):
        env = gym.make('gym_tensegrity:jumper-v0', config=config)
    if(config is None):
        env = gym.make('gym_tensegrity:jumper-v0') 
           
    observation = env.reset()
    print_observation(observation)
    tot_reward = 0
    action = np.array([0. for i in range(8)])
    done = False
    input("-> check point: WAIT for INPUT !!!!")

    while not done:
        # action = env.action_space.sample()
        print("Action: {:}".format(action))
        observation, reward, done, _= env.step(action)
        tot_reward += reward
        print("Reward: {:}, Done: {:}".format(reward,done))
        print("Time: {:}".format(env.env.getTime()))
        print_observation(observation)
        print("angle:{:}".format(env.env.getLegAngle()*180/np.pi))
        print("Total Reward: {:}".format(tot_reward))
        input("-> check point: WAIT for INPUT !!!!")

        # sleep(0.01)
    input("-> check point: WAIT for INPUT !!!!")

    while True:
        flag = 0
        inp = input("~~~~~~input: ")
        #action = env.action_space.sample()
        #observation, reward, done, _= env.step(action)

        if(inp == "w"):
            flag = 1
        elif(inp == "s"):
            flag = -1
        elif(inp == "d"):
            flag = 0

        if(flag < 0):
            action[0] = -0.1
            
        if(flag > 0):
            action[0] = 0.1

        if(flag == 0):
            action[0] = 0

        observation, reward, done, _= env.step(action)

        print(observation)
        print("angle:{:}".format(env.env.getLegAngle()*180/np.pi))

if __name__ == "__main__":
    test()
    # main_cont_dlengths({'observation':['end_points'], 'control_type': 'current_length_mod'})
    # main_cont_lengths()
    # main()
    # forked_process_main()
    # threaded_main()
