import pygame
from pygame.font import Font
from pygame.locals import Color
from Inputs import Input
from MyGame import *
from enum import Enum

clock = pygame.time.Clock()
ROW_SPACE = 20
ROW_HIGHT = 25
ROW_HIGHT_S = 20
CURSOR_SIZE = 20
BACKGROUND_COLOR = Color(60,60,60)
FONT = '8-BIT WONDER.TTF'
CREDITS = 'This clone made by achiyazigi.\nYou\'r more then welcome to visit my github profile at:\nhttps://github.com/achiyazigi'
class State(Enum):
        start=0
        options=1
        credits=2
        volume=3
        back=4

class Menu:
    
    def __init__(self, game:Game):
        self.input = Input()
        self.game = game
        self.center_w = game.screen.get_width()//2
        self.center_h = game.screen.get_height()//2
        self.run_display = True
        self.cursur_rect = pygame.Rect(0,0,20,20)
        self.offset = -100

    def draw_cursor(self):
        draw_text(self.game.screen, '*', (self.cursur_rect.x, self.cursur_rect.y), size=CURSOR_SIZE, font=FONT)

class MainMenu(Menu):
    def __init__(self, game: Game):
        super().__init__(game)
        self.options = OptionsMenu(self.game)
        # self.credits = OptionsMenu(self.game)
        self.state = State.start
        self.startx = self.center_w
        self.starty = self.center_h + ROW_HIGHT
        self.optionsx = self.center_w
        self.optionsy = self.starty + ROW_HIGHT
        self.creditsx = self.center_w
        self.creditsy = self.optionsy + ROW_HIGHT
        self.cursur_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while(self.run_display):
            self.check_input()
            self.game.screen.fill(BACKGROUND_COLOR)
            draw_text(self.game.screen, 'Main Menu', (self.game.screen.get_width() //2, self.game.screen.get_height()//2 - ROW_SPACE), size=ROW_HIGHT_S, font=FONT)
            draw_text(self.game.screen, 'Start Game',(self.startx, self.starty), size=ROW_HIGHT_S, font=FONT)
            draw_text(self.game.screen, 'Options',(self.optionsx, self.optionsy), size=ROW_HIGHT_S, font=FONT)
            draw_text(self.game.screen, 'Credits',(self.creditsx, self.creditsy), size=ROW_HIGHT_S, font=FONT)
            self.draw_cursor()
            pygame.display.update()
            clock.tick(60)

    
    def check_input(self):
        self.input.check_input()
        if(self.input.any_key_pressed):
            if(self.input.down):
                if(self.state == State.start):
                    self.cursur_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                    self.state = State.options
                elif(self.state == State.options):
                    self.cursur_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                    self.state = State.credits
                elif(self.state == State.credits):
                    self.cursur_rect.midtop = (self.startx + self.offset, self.starty)
                    self.state = State.start
            elif(self.input.up):
                if(self.state == State.credits):
                    self.cursur_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                    self.state = State.options
                elif(self.state == State.start):
                    self.cursur_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                    self.state = State.credits
                elif(self.state == State.options):
                    self.cursur_rect.midtop = (self.startx + self.offset, self.starty)
                    self.state = State.start
            elif(self.input.space):
                self.run_display = False
                if(self.state == State.start):
                    self.game.over = False
                elif(self.state == State.options):
                    self.options.display_menu()
                    self.run_display = True
                elif(self.state == State.credits):
                    pass
            self.input.reset()
        elif(self.input.quit):
            pygame.quit()
            exit()

class OptionsMenu(Menu):
    def __init__(self, game: Game):
        super().__init__(game)
        self.state = State.volume
        self.volx = self.center_w
        self.voly = self.center_h + ROW_SPACE
        self.backx = self.game.screen.get_width()//4
        self.backy = self.game.screen.get_height() - self.game.screen.get_height()//10
        self.cursur_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        screen = self.game.screen
        self.run_display = True

        while(self.run_display):
            self.check_input()
            screen.fill(BACKGROUND_COLOR)
            draw_text(screen, 'Options', (screen.get_width()//2, screen.get_height()//2 - ROW_HIGHT_S), size=ROW_HIGHT_S, font=FONT)
            draw_text(screen, 'Grid Size', (self.volx, self.voly), size=15, font=FONT)
            draw_text(screen, 'Back', (self.backx, self.backy), size=15, font=FONT)
            self.draw_cursor()
            pygame.display.update()
            clock.tick(60)
    def check_input(self):
        self.input.check_input()
        if(self.input.any_key_pressed):
            if(self.input.back or (self.input.space and self.state == State.back)):
                self.run_display = False

            elif(self.input.up or self.input.down):
                if(self.state == State.volume):
                    self.cursur_rect.midtop = (self.backx + self.offset//2, self.backy)
                    self.state = State.back
                else:
                    self.cursur_rect.midtop = (self.volx + self.offset, self.voly)
                    self.state = State.volume
            self.input.reset()
        elif(self.input.quit):
            pygame.quit()
            exit()
        


    

