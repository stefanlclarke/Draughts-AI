import pygame
from pygame import gfxdraw

class DraughtVisualiser:

    def __init__(self, screen_size, board_size):
        self.my_surf = pygame.Surface((screen_size,screen_size))
        self.b_size = board_size
        self.tile_size = screen_size / board_size

    def draw_square(self, x, y, colour):
        to_draw = pygame.Rect( x*self.tile_size, y*self.tile_size, self.tile_size , self.tile_size)
        gfxdraw.box(self.my_surf, to_draw, colour)

    def draw_piece(self, x, y, colour):
        gfxdraw.circle( self.my_surf,  int((x+0.5) *self.tile_size) , int((y + 0.5) * self.tile_size ) , int(self.tile_size * 0.4) ,colour )
        print("drawing")

    def draw_from_grid(self, grid):
        self.my_surf.fill(pygame.Color(0,0,0))
        for x in range(self.b_size):
            for y in range(self.b_size):
                val = grid[x][y]
                if val == 1 or  val == 3:
                    self.draw_piece(x,y, pygame.Color("chocolate1"))
                    #print("1")
                elif val == 2  or val == 4:
                    self.draw_piece(x,y, pygame.Color("chocolate2"))
                elif val == -1 or val == -3:
                    self.draw_piece(x,y, pygame.Color("tan1"))
                elif val == -2  or val == -4:
                    self.draw_piece(x,y, pygame.Color("tan2"))

                if val in [-4,-3,3,4]:
                    pygame.draw.circle(self.my_surf, pygame.Color("red"), ( int((x+0.5) *self.tile_size) , int((y + 0.5) * self.tile_size )) , int(self.tile_size * 0.1)  )



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
    vis = DraughtVisualiser(800,40)
    vis.draw_board()
    vis.draw_piece(3,3, pygame.Color("saddlebrown"))
    d_surf.blit(vis.my_surf, (0,0))
    pygame.display.set_caption("Test!")
    pygame.display.update()
    while True: # main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
