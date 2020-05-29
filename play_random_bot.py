import gym
import gym_draughts
from models import Actor, delete_diagonals, board_to_onehot, output_to_move, Memory
import torch as T
import numpy as np

actor = Actor(18, 10, 10, 18, 4)
memory = Memory(2000)

env = gym.make('draughts-v0')

def play_against_random():
    env.reset()
    playing = True
    while playing:
        currentmove = env.board.player
        if currentmove == -1:
            oldstate = env.get_state()
            loc, move, m = actor.forward_from_board(env.board.board)
            newstate, reward, done = env.step(m)
            memory.addstate(oldstate, loc, move, (newstate, reward, done))
            env.render()
        if currentmove == 1:
            mr = env.random_move()
            newstate, reward, done = env.step(mr)
            env.render()
        if done:
            playing = False


play_against_random()
