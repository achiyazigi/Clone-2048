import pygame
from pygame.constants import *


class Input:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.space = False
        self.back = False
        self.any_key_pressed = False
        self.quit = False


    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                break
            elif event.type == KEYDOWN:
                self.any_key_pressed = True
                if event.key == K_UP:
                    self.up = True
                elif event.key == K_DOWN:
                    self.down = True
                elif event.key == K_LEFT:
                    self.left = True
                elif event.key == K_RIGHT:
                    self.right = True
                elif event.key == K_SPACE:
                    self.space = True
                elif event.key == K_ESCAPE:
                    self.back = True

                break

    def reset(self):
        self.__init__()