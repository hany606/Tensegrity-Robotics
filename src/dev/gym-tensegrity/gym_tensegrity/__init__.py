from gym.envs.registration import register

# You here present all the environment you have
register(
    id='leg-v0',
    entry_point='gym_tensegrity.envs:LegEnv',
)

register(
    id='jumper-v0',
    entry_point='gym_tensegrity.envs:JumperEnv',
)

import gym_tensegrity.envs