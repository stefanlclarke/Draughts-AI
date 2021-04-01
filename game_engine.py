import numpy as np
import gym
import gym_draughts
import pygame
from display.draught_surf import DraughtVisualiser, find_square
from wrapper.wrapper import GameWrapper

class GameEngine:
    def __init__(self, yellow_player='human', pink_player='human'):

        """
        Class for human/bot/whatever play with/without visualiser. Simply load the class
        and run .run()
        """

        self.env = gym.make('draughts-v0')
        self.save_game = GameWrapper(self.env)
        self.human_yellow = False
        self.human_pink = False
        self.random_yellow = False
        self.random_pink = False



        if yellow_player == 'human':
            self.human_yellow = True
        if pink_player == 'human':
            self.human_pink = True

        if yellow_player == 'random':
            self.random_yellow = True
        if pink_player == 'random':
            self.random_pink = True

        self.yellow_player = yellow_player
        self.pink_plyer = pink_player

        self.moving_piece = 0
        self.last_click = None
        self.game_over = False

    def get_human_interactions(self):
        done = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.game_over = True
            if event.type == pygame.MOUSEBUTTONUP:

                pos = pygame.mouse.get_pos()
                square = find_square( (0,0), pos, 800/6)
                self.moving_piece = square
                self.last_click = square

            if event.type==pygame.KEYDOWN:
                key_name=pygame.key.name(event.key)
                if key_name=='w':
                    new_board, reward, done, illegal = self.save_game.step([self.moving_piece[0], self.moving_piece[1], 0])
                    self.last_click = None
                if key_name=='e':
                    new_board, reward, done, illegal = self.save_game.step([self.moving_piece[0], self.moving_piece[1], 3])
                    self.last_click = None
                if key_name=='d':
                    new_board, reward, done, illegal = self.save_game.step([self.moving_piece[0], self.moving_piece[1], 2])
                    self.last_click = None
                if key_name=='s':
                    new_board, reward, done, illegal = self.save_game.step([self.moving_piece[0], self.moving_piece[1], 1])
                    self.last_click = None

        return done

    def run(self):

        if self.human_pink or self.human_yellow:
            pygame.init()
            d_surf = pygame.display.set_mode((800,800))
            vis = DraughtVisualiser(800,6)
            vis.draw_board()
            d_surf.blit(vis.my_surf, (0,0))
            pygame.display.set_caption("Test!")
            vis.draw_from_grid(self.env.board.board)
            pygame.display.update()

        while not self.game_over: # main game loop
            if self.env.board.player == -1:
                if self.human_yellow:
                    self.game_over = self.get_human_interactions()
                elif self.random_yellow:
                    new_board, reward, self.game_over, illegal = self.save_game.step(self.env.random_move())
                else:
                    move = self.yellow_player.move(self.env.get_state())
                    new_board, reward, self.game_over, illegal = self.save_game.step(move)

            elif self.env.board.player == 1:
                if self.human_pink:
                    self.game_over = self.get_human_interactions()
                elif self.random_pink:
                    new_board, reward, self.game_over, illegal = self.save_game.step(self.env.random_move())
                else:
                    move = self.pink_player.move(self.env.get_state())
                    new_board, reward, self.game_over, illegal = self.save_game.step(move)

            if self.human_pink or self.human_yellow:
                if not self.game_over:
                    vis.draw_from_grid(self.env.board.board)
                    vis.draw_click_marker(self.last_click)
                    colour=pygame.Color("chocolate1")
                    d_surf.blit(vis.my_surf, (0,0))
                    pygame.display.update()


if __name__ == "__main__":
    # execute only if run as a script
    engine = GameEngine(pink_player='random')
    engine.run()
