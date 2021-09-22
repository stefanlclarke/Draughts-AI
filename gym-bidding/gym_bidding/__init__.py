from gym.envs.registration import register

register(
    id='bidding_unif-v0',
    entry_point='gym_bidding.envs:BiddingVsUniformEnvironment',
)
