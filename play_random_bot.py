import gym
import gym_draughts
from models import Actor, delete_diagonals, board_to_onehot, output_to_move, Memory
import torch as T
actor = Actor(18, 10, 10, 18, 4)
memory = Memory(2000)

env = gym.make('draughts-v0')
board = env.board.board
onehot = board_to_onehot(board)
onehot
loc, move = actor.forward(T.from_numpy(onehot).float())
loc = loc.detach().numpy()
move = move.detach().numpy()
oldstate = env.get_state()
m = output_to_move(loc, move)
m
newstate = env.step(m)
memory.addstate(oldstate, loc, move, newstate)
memory.memory
