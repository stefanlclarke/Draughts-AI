import gym
from gym import spaces
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
import random

class BiddingVsUniformEnvironment(gym.Env):
    """Bidding environment made by Stefan and Seb"""
    metadata = {'render.modes': []}

    def __init__(self):
        self.state = [10,100,100,0]
        #self.action_space

        return self.state

    def reset(self):
        self.state = [10,100,100,0]
        return self.state

    def get_ai_bid(self):
        return np.random.randint(0, self.state[2] + 1)

    def step(self, action):
        reward = 0.0
        if state[0] == 0:
            raise "Oh No this is bad"

        if action > self.state[1]:
            reward -= 0.01
            action = self.state[1]
        self.state[1] -= action

        ai_bid = self.get_ai_bid()
        self.state[2] -= ai_bid

        self.state[3] += 1*(action > ai_bid) - 1*(ai_bid > action)
        reward += 0.01 * (1*(action > ai_bid) - 1*(ai_bid > action))

        self.state[0] -= 1

        if self.state[0] == 0:
            reward += 1*(self.state[3] > 0)
            reward -= 1*(self.state[3] < 0)

        return self.state , reward , self.state[0] == 0 , {}


    def render(self, mode='human', close=False):
        print("Rendering! ☺")
        print(self.state)
        print("Rendering done! ☺")
        return



    def get_state(self):
        return self.state
