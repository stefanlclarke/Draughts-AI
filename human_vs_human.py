import numpy as np
import gym
import gym_draughts
import pygame
from draught_surf import DraughtVisualiser, find_square

class PvPEngine:
    def __init__(self):

        """
        Class for human v human play with visualiser. Simply load the class
        and run .run()
        """
        self.env = gym.make('draughts-v0')

    def run(self):
        pygame.init()
        d_surf = pygame.display.set_mode((800,800))
        vis = DraughtVisualiser(800,6)
        vis.draw_board()
        d_surf.blit(vis.my_surf, (0,0))
        pygame.display.set_caption("Test!")
        vis.draw_from_grid(self.env.board.board)
        pygame.display.update()
        MOVETHISPIECE = 0
        last_click = None

        while True: # main game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:

                    pos = pygame.mouse.get_pos()
                    square = find_square( (0,0), pos, 800/6)
                    MOVETHISPIECE = square
                    last_click = square

                if event.type==pygame.KEYDOWN:
                    key_name=pygame.key.name(event.key)
                    if key_name=='w':
                        self.env.step([MOVETHISPIECE[0], MOVETHISPIECE[1], 0])
                        last_click = None
                    if key_name=='e':
                        self.env.step([MOVETHISPIECE[0], MOVETHISPIECE[1], 3])
                        last_click = None
                    if key_name=='d':
                        self.env.step([MOVETHISPIECE[0], MOVETHISPIECE[1], 2])
                        last_click = None
                    if key_name=='s':
                        self.env.step([MOVETHISPIECE[0], MOVETHISPIECE[1], 1])
                        last_click = None

            vis.draw_from_grid(self.env.board.board)
            vis.draw_click_marker(last_click)
            colour=pygame.Color("chocolate1")
            d_surf.blit(vis.my_surf, (0,0))
            pygame.display.update()


if __name__ == "__main__":
    # execute only if run as a script
    engine = PvPEngine()
    engine.run()
