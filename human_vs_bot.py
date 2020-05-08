import numpy as np
from game import get_random_move
import play
import pygame
from pygame import gfxdraw
from play import game, play
from draught_surf import DraughtVisualiser, test, find_square
def makeboard():
    pygame.init()
    game.reset()
    d_surf = pygame.display.set_mode((800,800))
    vis = DraughtVisualiser(800,6)
    vis.draw_board()
    d_surf.blit(vis.my_surf, (0,0))
    pygame.display.set_caption("Test!")
    vis.draw_from_grid(game.board)
    pygame.display.update()
    MOVETHISPIECE=0
    moving=0
    while True: # main game loop
        if moving==1:
            AIMOVE=get_random_move(game.board, 1)
            play(AIMOVE[0][0], AIMOVE[0][1], AIMOVE[1])
            moving=0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:

                pos = pygame.mouse.get_pos()
                square = find_square( (0,0), pos, 800/6)
                MOVETHISPIECE=square
            if event.type==pygame.KEYDOWN:
                moving=1
                key_name=pygame.key.name(event.key)
                if key_name=='w':
                    play(MOVETHISPIECE[0], MOVETHISPIECE[1], 0)
                if key_name=='a':
                    play(MOVETHISPIECE[0], MOVETHISPIECE[1], 1)
                if key_name=='s':
                    play(MOVETHISPIECE[0], MOVETHISPIECE[1], 2)
                if key_name=='d':
                    play(MOVETHISPIECE[0], MOVETHISPIECE[1], 3)

        vis.draw_from_grid(game.board)
        colour=pygame.Color("chocolate1")
        d_surf.blit(vis.my_surf, (0,0))
        pygame.display.update()
makeboard()
