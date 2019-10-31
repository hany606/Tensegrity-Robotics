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
        obs = env.reset()
        for step in range(num_steps):
            # _states are only useful when using LSTM policies
            action, _states = model.predict(obs)
            print(action)
            history[-1].append(action)
            # here, action, rewards and dones are arrays
            # because we are using vectorized env
            obs, rewards, dones, info = env.step(action)
            
            episode_rewards[-1] += rewards[0]
            if dones[0]:
                successful_episode_rewards.append(0.0)
                successful_episode_rewards[-1] = episode_rewards[-1] 
                done_list[-1] = 1
                break
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


env = gym.make('gym_tensegrity:leg-v0')
# env = wrappers.Monitor(env, 'Tensegrity_leg_video', force=True)

env = DummyVecEnv([lambda: env])

model = DQN(MlpPolicy, env, verbose=1, learning_rate=0.1, exploration_fraction=0.5, tensorboard_log="/tmp/DQN_test_cartpole_tensorboard/")


# mean_reward_before_train = evaluate(model, num_episodes=10000, num_steps=10000)
mean_reward_before_train = evaluate(model, num_episodes=10, num_steps=1000, plt_tag='ro')

# input("Check point!!!")

model.learn(total_timesteps=10000)
model.save("DQN_tensegrity_leg")
print("Finish Training and saving the model")

del model

# input("Check point!!!")
model = DQN.load("DQN_tensegrity_leg")
mean_reward = evaluate(model, num_episodes=10, num_steps=1000, plt_tag='b^')

plt.show()

# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()