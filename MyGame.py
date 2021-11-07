from typing import Tuple
import pygame
from pygame import Color
from pygame.locals import *
from Inputs import Input
from Tile import Tile
from Tiles import Tiles


pygame.font.init()


def draw_text(screen: pygame.Surface, text: str, cordinates: tuple[int, int], color: Color = Color(255, 255, 255), size=30, font='Comic Sans MS'):
    try:
        myfont = pygame.font.Font(font, size)
    except:
        myfont = pygame.font.SysFont(font, size)
    lines = text.splitlines()
    for i, line in enumerate(lines):
        surf = myfont.render(line, True, color)
        text_rect = surf.get_rect()
        text_rect.center = (cordinates[0], cordinates[1] + i * size * 1.25)
        screen.blit(surf, text_rect)


class Game:
    def __init__(self, screen: pygame.Surface, tiles: Tiles, tiles_rect: Rect, animation_speed):
        self.input = Input()
        self.screen = screen
        self.tiles = tiles
        self.tiles_rect = tiles_rect
        self.changed = False
        self.over = False
        self.targets: dict[Tuple[int, int], Tile] = {}
        self.animation_speed = animation_speed

    def start(self):
        self.tiles.generate2or4()

    def draw_tiles(self):

        # draw tiles
        for i in range(self.tiles.size()):
            for j in range(self.tiles.size()):
                tile = self.tiles.get_tile(i, j)
                color = tile.get_color()
                if((i, j) in self.targets):
                    dst_i, dst_j = self.targets[(i,j)]
                    dst = self.tiles.get_tile(dst_i, dst_j)
                    color = dst.get_color()
                pygame.draw.rect(self.screen, color, tile.get_rect())
                if(tile.num > 0):
                    draw_text(self.screen, str(tile.num),
                              tile.get_center(), Color(255, 255, 255))

    def move(self):
        self.changed = False
        if(len(self.targets) == 0):
            if(self.input.down):
                self.changed |= self.tiles.down(self.targets)
            elif(self.input.up):
                self.changed |= self.tiles.up(self.targets)
            elif(self.input.left):
                self.changed |= self.tiles.left(self.targets)
            elif(self.input.right):
                self.changed |= self.tiles.right(self.targets)
            if(self.changed):
                self.tiles.generate2or4()
                if(self.tiles.game_over_check()):
                    self.over = True

    def update_tiles_state(self):
        # slide animation:
        
        to_remove_from_targets = set()

        for (i, j), (dst_i, dst_j) in self.targets.items():
            dst_x, dst_y = self.tiles.get_initial_position(dst_i, dst_j)
            src = self.tiles.get_tile(i, j)

            # draw a blank rect where the tile has originaly placed
            initial_x, initial_y = self.tiles.get_initial_position(i, j)
            clone = Tile(initial_x, initial_y,
                         self.tiles.tile_size, src.margin, 0)
            pygame.draw.rect(self.screen, clone.get_color(), clone.get_rect())

            if(abs(src.x - dst_x + src.y - dst_y) > 20):
                src.x -= (src.x - dst_x) * self.animation_speed
                src.y -= (src.y - dst_y) * self.animation_speed
            else:
                if((i, j) not in to_remove_from_targets):
                    src.x, src.y = self.tiles.get_initial_position(i, j)
                to_remove_from_targets.add((i, j))
        for key in to_remove_from_targets:
            self.targets.pop(key)
