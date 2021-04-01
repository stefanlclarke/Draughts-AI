import numpy as np
import pickle
from datetime import datetime
from copy import deepcopy

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
