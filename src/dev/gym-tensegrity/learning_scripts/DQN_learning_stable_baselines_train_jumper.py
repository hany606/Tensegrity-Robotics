#using stable-baselines
import gym_tensegrity

import gym
from gym import wrappers
import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN


def evaluate(model, num_episodes= 1000, num_steps=1000, plt_tag='ro'):
    """
    Evaluate a RL agent
    :param model: (BaseRLModel object) the RL Agent
    :param num_steps: (int) number of timesteps to evaluate it
    :return: (float) Mean reward for the last 100 episodes
    """
    successful_episode_rewards = []
    episode_rewards = []
    history = []
    done_list = []
    for episode in tqdm(range(num_episodes)):
        episode_rewards.append(0.0)
        history.append([])
        done_list.append(0)
        input("Waiting for an input")
        obs = env.reset()
        successful_flag = True
        for i in range(num_steps):
            # _states are only useful when using LSTM policies
            print(obs)
            action, _states = model.predict(obs)
            print("Action: ", action[0])
            history[-1].append(action)
            # here, action, rewards and dones are arrays
            # because we are using vectorized env
            obs, rewards, done, info = env.step(action)
            
            episode_rewards[-1] += rewards[0]
            print(done)
            input("Waiting for an input2")

            if done[0]:
                successful_flag = False
                print("Faild(((")
                # TODO: Why it is reseting by itself here??????
                # Maybe something related to gym when I comment break as it is not get out the episode but reset itself
                break

        if(successful_flag):
            successful_episode_rewards.append(0.0)
            successful_episode_rewards[-1] = episode_rewards[-1] 
            done_list[-1] = 1
    print(episode_rewards)
    print(successful_episode_rewards)
    for i in range(len(done_list)):
        if(done_list[i] == 1):
            print("Episode {:} is successful to the target with reward: {:}".format(i, episode_rewards[i]))
    mean_reward = round(np.mean(episode_rewards), 3)
    print("Mean reward: {:}, Num successfull episodes: {:}/{:}".format(mean_reward, len(successful_episode_rewards), num_episodes))

    plt.plot(episode_rewards,plt_tag)
    # plt.axis([0, num_episodes , ])
    plt.ylabel('Rewards')
    plt.xlabel('Episodes')
    # plt.show()
    return mean_reward


env = gym.make('gym_tensegrity:jumper-v0')
# env = gym.make("CartPole-v1")
# env = wrappers.Monitor(env, 'Tensegrity_leg_video', force=True)

env = DummyVecEnv([lambda: env])

model = DQN(MlpPolicy, env, verbose=1, learning_rate=0.1, exploration_fraction=0.5, tensorboard_log="/tmp/DQN_test_cartpole_tensorboard/")


# mean_reward_before_train = evaluate(model, num_episodes=10000, num_steps=10000)
mean_reward_before_train = evaluate(model, num_episodes=10, num_steps=150, plt_tag='r')
# plt.show()
# input("Check point!!!")

model.learn(total_timesteps=150*10)
model.save("DQN_tensegrity_jumper_short_training")
print("Finish Training and saving the model")

del model

# input("Check point!!!")
model = DQN.load("DQN_tensegrity_jumper_short_training")
mean_reward = evaluate(model, num_episodes=10, num_steps=150, plt_tag='b')

plt.show()

# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()