from random import Random
from MyGame import Game
import pygame
from Tiles import Tiles
from pygame import Rect
from pygame.locals import *
from pygameMenuPro import *
from MyMenu import create_my_menu

from Inputs import Input


clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('title')

input = Input()
r = Random()
WIDTH, HEIGHT = 360, 640
WINDOW_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(WINDOW_SIZE, depth=32)

TILES_RECT_SIZE = 300
TILES_RECT_POS = ((WIDTH-TILES_RECT_SIZE)//2, (HEIGHT - TILES_RECT_SIZE)//2)

TITLE_POS = (WIDTH//2, HEIGHT//2 - 100)

BACKGROUND_COLOR = Color(23,170,84)

tiles_rect = Rect(*TILES_RECT_POS, TILES_RECT_SIZE, TILES_RECT_SIZE)
tiles = Tiles(TILES_RECT_POS, TILES_RECT_SIZE)

game = Game(screen, tiles, tiles_rect, 0.5)
game.over = True

def main_loop():
    while (not game.over):

        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, Color(20, 20, 20), tiles_rect)

        game.update_tiles_state()
        # draw tiles
        game.draw_tiles()

        game.input.check_input()
        if(game.input.back):
            game.pause()
        # move
        # ----------------------------
        # self play...
        # if(len(game.targets) == 0):
        #     dir = r.randint(0, 3)

        #     if dir ==  0:
        #         game.input.down = True
        #     elif dir == 1:
        #         game.input.up = True
        #     elif dir == 2:
        #         game.input.left = True
        #     else: 
        #         game.input.right = True
        #     game.move()
        # ----------------------------
        if(game.input.any_key_pressed):
            game.move()
        elif(game.input.quit):
            pygame.quit()
            exit()
        game.input.reset()

        pygame.display.update()
        clock.tick(60)

    # Game Over
    game.draw_tiles()
    pygame.display.update()
    pygame.time.wait(2000)
    Option.input.reset_last_checked()
    main_menu.display_menu()


main_menu = create_my_menu(screen, game, TITLE_POS, main_loop)
main_menu.display_menu()
pygame.quit()
exit()
