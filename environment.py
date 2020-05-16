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
        self.capture_reward = 0.1
        self.king_reward = 0.2

    def reset(self):
        board.reset()

    def step(self, action):
        victor, stalemate, took, king = self._take_action(action)
        new_board = np.copy(self.board.board)
        reward = 0
        if victor != 0:
            reward += self.win_reward
            done = True
        elif stalemate != 0:
            reward += self.stalemate_reward
            done = True
        else:
            done = False
        if took == True:
            reward += self.capture_reward
        if king == True:
            reward += self.king_reward
        return new_board, reward, done

    def _take_action(self, action):
        victor, stalemate, took, king = self.board.makemove(np.array([action[0], action[1]]), action[2])
        return victor, stalemate, took, king

    def render(self, mode='human', close=False):
        print(self.board.board)

    def _next_observation(self):
        return board.board
