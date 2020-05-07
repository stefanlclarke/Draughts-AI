import pygame
from pygame import gfxdraw

def find_square( corner , click , square_size):
    # Finds the square clicked on from the pixel and corner
    square_x = int((click[0] -  corner[0]) // square_size)
    square_y = int((click[1] -  corner[1]) // square_size)
    return (square_x, square_y)


class DraughtVisualiser:
    def __init__(self, screen_size, board_size):
        self.my_surf = pygame.Surface((screen_size,screen_size))
        self.b_size = board_size
        self.tile_size = screen_size / board_size

    def draw_square(self, x, y, colour):
        to_draw = pygame.Rect( x*self.tile_size, y*self.tile_size, self.tile_size , self.tile_size)
        gfxdraw.box(self.my_surf, to_draw, colour)

    def draw_piece(self, x, y, colour):
        gfxdraw.filled_circle( self.my_surf,  int((x+0.5) *self.tile_size) , int((y + 0.5) * self.tile_size ) , int(self.tile_size * 0.4) ,colour )

    def draw_from_grid(self, grid):
        self.my_surf.fill(pygame.Color(0,0,0))
        self.draw_board()
        for x in range(self.b_size):
            for y in range(self.b_size):
                val = grid[x][y]
                if val == 1 or  val == 3:
                    self.draw_piece(x,y, pygame.Color("chocolate1"))
                    #print("1")
                elif val == 2  or val == 4:
                    self.draw_piece(x,y, pygame.Color("chocolate4"))
                elif val == -1 or val == -3:
                    self.draw_piece(x,y, pygame.Color("darkgoldenrod1"))
                elif val == -2  or val == -4:
                    self.draw_piece(x,y, pygame.Color("darkgoldenrod4"))

                if val in [-4,-3,3,4]:
                    gfxdraw.filled_circle(self.my_surf,   int((x+0.5) *self.tile_size) , int((y + 0.5) * self.tile_size ) , int(self.tile_size * 0.1) , pygame.Color("red") )




    def draw_board(self):
        for x in range(self.b_size):
            for y in range(self.b_size):
                if (x+y)%2 == 0:
                    self.draw_square(x,y, pygame.Color("black"))
                else:
                    self.draw_square(x,y, pygame.Color("brown"))

def test():
    pygame.init()
    d_surf = pygame.display.set_mode((800,800))
    board = [[0 for i in range(40)] for j in range(40)]
    vis = DraughtVisualiser(800,40)
    vis.draw_board()

    pygame.display.set_caption("Test!")
    pygame.display.update()
    while True: # main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                square = find_square( (0,0), pos, 800/40)
                board[square[0]][square[1]] += 1
                if board[square[0]][square[1]] >  4:
                    board[square[0]][square[1]] = -4

        vis.draw_from_grid(board)
        d_surf.blit(vis.my_surf, (0,0))
        pygame.display.update()
