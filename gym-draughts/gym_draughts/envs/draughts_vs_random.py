import numpy as np
import gym
import pygame
from gym_draughts.envs.draughts_wrapper import DraughtsWrapper, move_to_index

class DraughtsRandom(gym.Env):
    def __init__(self):

        self.save_game = DraughtsWrapper()
        self.env = self.save_game.env

        self.action_space = self.save_game.action_space
        self.observation_space = self.save_game.observation_space


    def _next_observation(self):
        return self.save_game._next_observation()

    def step(self, move):
        new_board, reward, done, illegal = self.save_game.step(move)
        next_move = self.env.board.player
        print(next_move)

        if not done:
            while next_move == 1:
                random = move_to_index(self.env.random_move(), self.env.size)
                print(random)
                new_board_, reward_, done_, illegal_ = self.save_game.step(random)
                next_move = self.env.player

                reward -= reward_
                done = done_
                new_board = new_board_

        return new_board, reward, done, illegal

    def render(self):
        self.save_game.render()

    def reset(self):
        self.save_game.reset()
