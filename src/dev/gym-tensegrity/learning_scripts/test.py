
import gym
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import DQN
import numpy as np


def evaluate(model, num_episodes= 1000, num_steps=1000):
  """
  Evaluate a RL agent
  :param model: (BaseRLModel object) the RL Agent
  :param num_steps: (int) number of timesteps to evaluate it
  :return: (float) Mean reward for the last 100 episodes
  """
  episode_rewards = [0.0]
  for x in range(num_episodes):
    obs = env.reset()
    for i in range(num_steps):
        # _states are only useful when using LSTM policies
        action, _states = model.predict(obs)
        # here, action, rewards and dones are arrays
        # because we are using vectorized env
        obs, rewards, dones, info = env.step(action)
        
        episode_rewards[-1] += rewards[0]
        if dones[0]:
            episode_rewards.append(0.0)
            break

  mean_reward = round(np.mean(episode_rewards), 3)
  print("Mean reward: {:}, Num successfull episodes: {:}".format(mean_reward, len(episode_rewards)))
  
  return mean_reward


env = gym.make('CartPole-v1')
env = DummyVecEnv([lambda: env])  # The algorithms require a vectorized environment to run

model = DQN(MlpPolicy, env, verbose=1, tensorboard_log="/tmp/DQN_test_cartpole_tensorboard/")

mean_reward_before_train = evaluate(model, num_steps=10000)

model.learn(total_timesteps=10000)
model.save("test_cartpole_model")
print("Finish Training and saving the model")

del model

model = DQN.load("test_cartpole_model")
mean_reward = evaluate(model, num_steps=10000)

# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()