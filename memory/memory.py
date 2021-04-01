import numpy as np
import pickle
from datetime import datetime
from copy import deepcopy

def remove_diags(board, top_left = True):
    w = len(board[0])
    if w%2 != 0:
        raise ValueError(("board no good! Width not even!", board))
    h = len(board)
    to_ret = np.zeros((h,w/2))
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

class GameMemory:
    def __init__(self, game_env, save_as_onehot=True):
        """
        Class for pickling game-states to memory
        """
        self.memory = []
        self.move_memory = []
        self.env = game_env

        self.save_as_onehot = save_as_onehot

        if self.save_as_onehot:
            self.memory.append(board_to_onehot(deepcopy(self.env.get_state())))
        else:
            self.memory.append(deepcopy(self.env.get_state()))

    def save_game(self):
        save_name = "memory/saved_games/{}.pickle".format(str(datetime.now())).replace(" ","")
        pickle.dump([self.memory, self.move_memory], open( save_name.replace(":",""), "wb" ))

    def step(self, move, torch_agent=False):

        if torch_agent:
            move_ = index_to_move(index, self.env.size)
        else:
            move_ = deepcopy(move)
            move = move_to_index(move)

        new_board, reward, done, illegal = self.env.step(move_)

        if self.save_as_onehot:
            self.memory.append(board_to_onehot(deepcopy(self.env.get_state())))
            self.move_memory.append(move)
        else:
            self.memory.append(deepcopy(self.env.get_state()))
            self.move_memory.append(move_)

        if done:
            print('GAME OVER')
            self.save_game()
        return new_board, reward, done, illegal
