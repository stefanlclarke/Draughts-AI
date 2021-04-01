import gym
import gym_draughts
import pygame
import numpy as np

import pickle

import human_vs_human
import display.draught_surf as dSurf

class GameDisplayer():
    def __init__(self,  screen_size,  game_to_disp, extra_info = None, extra_names = None, extra_colours = None):
        
        # Extra info is a list of lists of [0,1] reals. Used for showing extra information
        self.board_size = len(game_to_disp[0])
        self.screen_size = screen_size
        self.game_to_disp = game_to_disp
        
        self.game_visualise = dSurf.DraughtVisualiser(screen_size , self.board_size)
        self.game_visualise.draw_from_grid(game_to_disp[0])
        
        self.extra_info = extra_info
        self.extra_names = extra_names
        self.extra_colours = extra_colours
        
        
        
        self.done = False
        
        self.current_frame = 0
        self.max_frame = len(self.game_to_disp)
        
        self.info_surf = pygame.Surface((200,screen_size))

        
    def show_stuff(self):
        pygame.init()
        
        self.main_surf = pygame.display.set_mode((self.screen_size + 200,self.screen_size))
        
        pygame.display.set_caption("Test!")
        pygame.display.update()
        
        self.font_render = pygame.font.SysFont(None, 24)
        
        img = self.font_render.render('hello', True, "blue")
        
        self.main_surf.blit(img, (20, 20))
        
        self.t = 0
        
        pygame.display.update()
        
    
        
        while not self.done:
            self.run_through_events()
            self.update_info()
            self.update_grid()
            pygame.display.update()
        self.quit()
        
    def update_info(self):
        self.info_surf.fill(pygame.Color(255, 255, 255))
        info_text = self.font_render.render(f'Frame {self.current_frame + 1}/{self.max_frame}', True, "black")
        self.info_surf.blit(info_text , (0,0))
        if not (self.extra_names is None):
            self.update_extra_info()
        self.main_surf.blit(self.info_surf, (self.screen_size ,0))
            
    def update_extra_info(self):
        for i in range(len(self.extra_names)):
            y_level = 30 * (i + 1)
            contex_text = self.font_render.render(self.extra_names[i], True, "black")
            self.info_surf.blit(contex_text , (0,y_level))
            full_rect = pygame.Rect(100, y_level, int(100 * self.extra_info[self.current_frame][i]) , 30)
            partial_rect = pygame.Rect(100, y_level + 25, 100, 5)
            if self.extra_colours is None:
                pygame.draw.rect(self.info_surf, "black", full_rect)
                pygame.draw.rect(self.info_surf, "black", partial_rect)
            else:
                pygame.draw.rect(self.info_surf, self.extra_colours[i], full_rect)
                pygame.draw.rect(self.info_surf, self.extra_colours[i], partial_rect)
                                
            
    
    def update_grid(self):
        self.game_visualise.draw_from_grid(self.game_to_disp[self.current_frame])
        self.main_surf.blit(self.game_visualise.my_surf, (0 ,0))
        
    def move_frame(self, delta):
        self.current_frame = np.clip(self.current_frame + delta,0, self.max_frame - 1)
        
    def run_through_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.mod & pygame.KMOD_SHIFT:
                    mod_factor = 10
                else:
                    mod_factor = 1
                if event.key == pygame.K_RIGHT:
                    self.move_frame(1 * mod_factor)
                if event.key == pygame.K_LEFT:
                    self.move_frame(-1 * mod_factor)
                
        
    def quit(self):
        pygame.display.quit()
        self.done = False