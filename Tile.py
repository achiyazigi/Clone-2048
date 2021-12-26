import pygame

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


class Tile:
    INITIAL_COLOR = 56
    COLOR_FACTOR = 1
    def __init__(self, x, y, size, margin, num):
        self.x = x
        self.y = y
        self.size = size
        self.margin = margin
        self.num = num

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x+self.margin, self.y+self.margin, self.size-2*self.margin, self.size-2*self.margin)

    def get_text_surface(self) -> pygame.Surface:
        return myfont.render(str(self.num), True, pygame.Color(255, 255, 255))

    def get_center(self) -> tuple[int, int]:
        return (self.x + self.size//2, self.y + self.size//2)

    def get_color(self):
        return Tile.get_color_from_num(self.num)

    def get_color_from_num(num):
        num = num * Tile.COLOR_FACTOR
        return pygame.Color((77*num) % 200 + Tile.INITIAL_COLOR, (125*num) % 200 + Tile.INITIAL_COLOR, (113*num) % 200 + Tile.INITIAL_COLOR)
