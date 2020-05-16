import gym
from gym import spaces
from gamefile import board
import numpy as np

class DraughtsEnvironment(gym.Env):
    """Druaghts environment made by Stefan and Seb"""
    metadata = {'render.modes': ['human']}

    def __init__(self, size):
        self.size=size
        self.board=board(self.size)

        self.win_reward = 10
        self.stalemate_reward = 2

    def reset(self):
        board.reset()

    def step(self, action):
        victor, stalemate = self._take_action(action)
        new_board = np.copy(self.board)
        if victor != 0:
            reward = self.win_reward
            done = True
        elif stalemate != 0:
            reward = self.stalemate_reward
            done = True
        else:
            done = False
            reward = 0
        return new_board, reward, done

    def _take_action(self, action):
        victor, stalemate = self.board.makemove(action[0], action[1])
        return victor, stalemate

    def render(self, mode='human', close=False):
        print(self.board.board)

    def _next_observation(self):
        return board.board

env=DraughtsEnvironment(6)
env.render()
env.step([np.array([4,0]), 1])
env.render()
