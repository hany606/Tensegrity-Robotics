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

register(
    id='twice-cube-v0',
    entry_point='gym_tensegrity.envs:TwiceCubeEnv',
)

register(
    id='test-v0',
    entry_point='gym_tensegrity.envs:TestEnv',
)