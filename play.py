import game
from game import board
import numpy as np

board_size=6
game = board(board_size)

def play(loc1, loc2, move):
    victor, stalemate = game.makemove(np.array([loc1, loc2]), move)
    #print(f"Victor: {victor}")
    #print(f"Stalemate? {stalemate}")
    #print("Game Board:")
    #print(game.board)
    if victor != 0:
        print("GAME OVER!")
        #game.reset()
    elif stalemate:
        print("STALEMATE")
        #game.reset()
    return victor
