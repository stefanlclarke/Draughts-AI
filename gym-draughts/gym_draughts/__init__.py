from gym.envs.registration import register

register(
    id='draughts-v0',
    entry_point='gym_draughts.envs:DraughtsEnvironment',
)
