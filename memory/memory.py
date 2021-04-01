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
    
    
class GameMemory:
    def __init__(self, game_env):
        """
        Class for pickling game-states to memory
        """
        self.memory = []
        self.move_memory = []
        self.env = game_env

        self.memory.append(deepcopy(self.env.get_state()))

    def save_game(self):
        save_name = "memory/saved_games/{}.pickle".format(str(datetime.now())).replace(" ","")
        pickle.dump([self.memory, self.move_memory], open( save_name.replace(":",""), "wb" ))

    def step(self, move):
        new_board, reward, done, illegal = self.env.step(move)
        self.memory.append(deepcopy(self.env.get_state()))
        self.move_memory.append(move)
        if done:
            print('GAME OVER')
            self.save_game()
        return new_board, reward, done, illegal
