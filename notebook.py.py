import numpy as np
import play
import pygame
from pygame import gfxdraw
from play import game, play
from draught_surf import DraughtVisualiser, test
def makeboard():
    pygame.init()
    d_surf = pygame.display.set_mode((800,800))
    vis = DraughtVisualiser(800,6)
    vis.draw_board()
    d_surf.blit(vis.my_surf, (0,0))
    pygame.display.set_caption("Test!")
    vis.draw_from_grid(game.board)
    pygame.display.update()

    while True: # main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        vis.draw_from_grid(game.board)
        x=1
        y=1
        colour=pygame.Color("chocolate1")
        gfxdraw.circle( vis.my_surf,  int((0) *vis.tile_size) , int((0) * vis.tile_size ) , int(vis.tile_size * 0.4) ,colour )
        d_surf.blit(vis.my_surf, (0,0))
        pygame.display.update()

makeboard()
