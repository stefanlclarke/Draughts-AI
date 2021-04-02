from gym.envs.registration import register

register(
    id='draughts-v0',
    entry_point='gym_draughts.envs:DraughtsEnvironment',
)

register(
    id='draughtswrapper-v0',
    entry_point='gym_draughts.envs:DraughtsWrapper',
)

register(
    id='draughtsrandom-v0',
    entry_point='gym_draughts.envs:DraughtsRandom',
)
