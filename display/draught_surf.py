import pygame
from pygame import gfxdraw
import numpy as np

def find_square( corner , click , square_size):
    # Finds the square clicked on from the pixel and corner
    square_x = int((click[0] -  corner[0]) // square_size)
    square_y = int((click[1] -  corner[1]) // square_size)
    return (square_x, square_y)

def aa_circle(surf, x ,y, size, col):
    gfxdraw.aacircle(surf, x ,y, size, col)
    gfxdraw.filled_circle(surf, x ,y, size, col)

class DraughtVisualiser:
    "Helps displaying by providing a pygame surface that may be updated from an array."
    def __init__(self, screen_size, board_size):
        self.my_surf = pygame.Surface((screen_size,screen_size))
        self.b_size = board_size
        self.tile_size = screen_size / board_size

    def draw_square(self, x, y, colour):
        "Draws a single square at tile x,y w with colour"
        to_draw = pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size , self.tile_size)
        gfxdraw.box(self.my_surf, to_draw, colour)

    def draw_piece(self, x, y, colour):
        "Draws a piece at the tile x,y in the colour given"
        aa_circle(self.my_surf, int((x+0.5) *self.tile_size) , int((y + 0.5) * self.tile_size ) , int(self.tile_size * 0.4) ,colour )

    def draw_from_grid(self, grid):
        self.my_surf.fill(pygame.Color(0, 0, 0))
        self.draw_board()
        for x_cord in range(self.b_size):
            for y in range(self.b_size):
                val = grid[x_cord][y]
                if val == 1 or  val == 3:
                    self.draw_piece(x_cord, y, pygame.Color("deeppink1"))
                elif val == 2  or val == 4:
                    self.draw_piece(x_cord, y, pygame.Color("darkorchid4"))
                elif val == -1 or val == -3:
                    self.draw_piece(x_cord, y, pygame.Color("darkgoldenrod1"))
                elif val == -2  or val == -4:
                    self.draw_piece(x_cord, y, pygame.Color("chocolate1"))

                if val in [-4,-3,3,4]:
                    aa_circle(self.my_surf,   int((x_cord+0.5) *self.tile_size) , int((y + 0.5) * self.tile_size ) , int(self.tile_size * 0.1) , pygame.Color("red") )

    def draw_click_marker(self, square):
        if square is not None:
            x = square[0]
            y = square[1]
            aa_circle(self.my_surf,   int((x+0.25) *self.tile_size) , int((y + 0.5) * self.tile_size ) , int(self.tile_size * 0.05) , pygame.Color("blue") )


    def draw_board(self):
        for x in range(self.b_size):
            for y in range(self.b_size):
                if (x+y)%2 == 0:
                    self.draw_square(x,y, pygame.Color("black"))
                else:
                    self.draw_square(x,y, pygame.Color("brown"))

def dummmy():
    print("DUM3")

def test():
    game_over = False
    pygame.init()
    d_surf = pygame.display.set_mode((800,800))
    board = [[0 for i in range(40)] for j in range(40)]
    vis = DraughtVisualiser(800,40)
    vis.draw_board()

    pygame.display.set_caption("Test!")
    pygame.display.update()
    while True: # main game loop
        clicknum = 0
        movepair = [np.array([0,0]), np.array([0,0])]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_over = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                square = find_square( (0,0), pos, 800/40)
                board[square[0]][square[1]] += 1
                if board[square[0]][square[1]] >  4:
                    board[square[0]][square[1]] = -4
                if clicknum == 0%2:
                    movepair[0] = square
                if clicknum == 1%2:
                    movepair[1] = square

        if not game_over:
            vis.draw_from_grid(board)
            d_surf.blit(vis.my_surf, (0,0))
            pygame.display.update()
