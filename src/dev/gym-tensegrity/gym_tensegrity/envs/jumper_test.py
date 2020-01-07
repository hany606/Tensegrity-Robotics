import gym
import gym_tensegrity
import numpy as np
import os

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
def main_cont_dlengths(port_num=10042):
    def print_observation(obs):
        print("Observations {:}".format(obs))
    env = gym.make('gym_tensegrity:jumper-v0')
    # action = randint(0,15)
    action = np.array([0 for i in range(8)])
    # action[0] = 5
    print("Action: {:}".format(action))
    # input("-> check point: WAIT for INPUT !!!!")
    init_obs ,_,_,_=env.step(action)

    print_observation(init_obs)
    print(type(init_obs))
    # print(env.env.actions_json)
    # print("")

    input("-> check point: WAIT for INPUT !!!!")

    while True:
        # action = env.action_space.sample()
        observation, reward, done, _= env.step(action)
        print(type(observation))
        print(action)
        input("-> check point: WAIT for INPUT !!!!")
        print("Reward: {:}, Done: {:}".format(reward,done))
        print_observation(observation)
        print("angle:{:}".format(observation[-1]*180/np.pi))


if __name__ == "__main__":
    main_cont_dlengths()
    # main_cont_lengths()
    # main()
    # forked_process_main()
    # threaded_main()