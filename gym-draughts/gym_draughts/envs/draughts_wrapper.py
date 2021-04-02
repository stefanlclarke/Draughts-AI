import numpy as np
import pickle
from datetime import datetime
from copy import deepcopy
import gym
from gym_draughts.envs.draughts_env import DraughtsEnvironment
from gym import spaces

def remove_diags(board, top_left = True):
    w = len(board[0])
    if w%2 != 0:
        raise ValueError(("board no good! Width not even!", board))
    h = len(board)
    to_ret = np.zeros((h,w//2))
    if top_left:
        to_ret[::2] = board[::2,::2]
        to_ret[1::2] = board[1::2,1::2]
    else:
        to_ret[::2] = board[::2,1::2]
        to_ret[1::2] = board[1::2,::2]
    return to_ret

def add_diags(board, top_left = True):
    w = len(board[0])
    h = len(board)
    to_ret = np.zeros((h,w*2))
    if top_left:
        to_ret[::2,::2] = board[::2]
        to_ret[1::2,1::2]= board[1::2]
    else:
        t_ret[::2,1::2] = board[::2]
        to_ret[1::2,::2] = board[1::2]
    return to_ret

def move_to_index(move, max_height):
    # Assume move is (x,y,dir). xs are merged together because diagonals
    x_contribution = move[0]//2 * max_height * 4
    y_contribution = move[1] * 4
    return x_contribution + y_contribution + move[2]

def index_to_move(index, max_height, top_left = True):
    direction = index % 4
    y_move = (index//4) % (max_height)
    x_move = (index // (4 * max_height)) * 2 # Times 2 is for collapsing.
    x_adjustment = (y_move + top_left + 1) % 2
    x_move += x_adjustment
    return (x_move, y_move, direction)

def board_to_onehot(board, possible_vals = None):
    if possible_vals is None:
        #default for a board
        possible_vals = np.array(list(range(-4,5)))
    n = len(possible_vals)
    to_ret = np.zeros((n,) + board.shape)
    # Feels like there should be a nice numpy way of doing this. Oh well lol
    for i in range(n):
        to_ret[i] = (board == possible_vals[i])
    return to_ret

def onehot_to_board(one_hot, possible_vals = None):
    if possible_vals is None:
        #default for a board
        possible_vals = np.array(list(range(-4,5)))
    return one_hot.tranpose() @ possible_vals

def board_transform(board):
    return board_to_onehot(remove_diags(board))

class DraughtsWrapper(gym.Env):
    def __init__(self, save_as_onehot=True, save_loc='saved_games/'):
        super(DraughtsWrapper, self).__init__()
        """
        Class for pickling game-states to memory and making the game pytorch-able.
        """
        self.memory = []
        self.move_memory = []
        self.env = DraughtsEnvironment()

        self.save_as_onehot = save_as_onehot

        if self.save_as_onehot:
            self.memory.append(board_transform(deepcopy(self.env.get_state())))
        else:
            self.memory.append(deepcopy(self.env.get_state()))

        #gym parameters
        self.observation_space = spaces.Discrete(9 * self.env.size **2 /2)
        self.action_space = spaces.Discrete(2 * self.env.size**2)

    def save_game(self):
        save_name = save_loc+"{}.pickle".format(str(datetime.now())).replace(" ","")
        pickle.dump([self.memory, self.move_memory], open( save_name.replace(":",""), "wb" ))

    def step(self, move, torch_agent=True):

        if torch_agent:
            move_ = index_to_move(index, self.env.size)
        else:
            move_ = deepcopy(move)
            move = move_to_index(move, self.env.size)

        new_board, reward, done, illegal = self.env.step(move_)
        onehot_board = board_transform(new_board)

        if self.save_as_onehot:
            self.memory.append(deepcopy(onehot_board))
            self.move_memory.append(move)
        else:
            self.memory.append(deepcopy(new_board))
            self.move_memory.append(move_)

        if done:
            self.save_game()

        if self.save_as_onehot:
            return onehot_board, reward, done, illegal
        else:
            return new_board, reward, done, illegal

    def reset(self):
        self.memory = []
        self.move_memory = []
        self.env.reset()
        curr_board = board_transform(self.env._next_observation())

        return curr_board, 0, False, False

    def _next_observation(self):
        return board_transform(self.env._next_observation())

    def render(self, mode='human', close=False):
        print(self.env.board.board)
