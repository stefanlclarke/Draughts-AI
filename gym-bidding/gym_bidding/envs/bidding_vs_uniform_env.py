import gym
from gym import spaces
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
import random

class BiddingEnvironment(gym.Env):
    """Bidding environment made by Stefan and Seb"""
    metadata = {'render.modes': []}

    def __init__(self):
        self.state = [10,100,100,0]
        return

    def reset(self):
        self.state = [10,100,100,0]
        return


    def step(self, action):
        if state[0] == 0:
            
        if action > self.state[1]:
            apply_punishment
        self.state[1] -= action

        ai_bid = np.random.randint(0, self.state[2] + 1)
        self.state[2] -= ai_bid

        self.state[3] += 1*(action > ai_bid) - 1*(ai_bid > action)
        state[0] -= 1
        return

    def _take_action(self, action):
        pass

    def render(self, mode='human', close=False):
        pass

    def _next_observation(self):
        return self.get_state()

    def get_state(self):
        pass
