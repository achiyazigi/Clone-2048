from types import FunctionType
from typing import Tuple
import pygame
from pygame import Color, Rect
from pygame import time
from pygame import display
from pygame.display import update
from Tile import Tile
import random


TILE_MARGIN = 5
clock = pygame.time.Clock()


class Tiles:
    def __init__(self, tiles_rect_pos, tiles_rect_size, size=4):
        self.tile_size = tiles_rect_size//size
        self.x = tiles_rect_pos[0]
        self.y = tiles_rect_pos[1]
        self.rect_size = tiles_rect_size

        self._open_tiles = {}
        self.reset_tiles()
        self._update_open_tiles()

    def reset_tiles(self):
        self._tiles = [
            [
                Tile(*self.get_initial_position(i, j),
                     self.tile_size, TILE_MARGIN, 0)
                for j in range(self.rect_size//self.tile_size)
            ]
            for i in range(self.rect_size//self.tile_size)
        ]
    def _update_open_tiles(self):
        for row in self._tiles:
            for tile in row:
                if(tile.num == 0):
                    self._open_tiles[(tile.x, tile.y)] = tile
                elif((tile.x, tile.y) in self._open_tiles):
                    self._open_tiles.pop((tile.x, tile.y))

    def get_tile(self, row: int, col: int) -> Tile:

        return self._tiles[int(row)][int(col)]

    def size(self):
        return len(self._tiles)

    def generate2or4(self):
        if(len(self._open_tiles) == 0):
            return
        chosen_tile = random.choice(list(self._open_tiles.items()))
        self._open_tiles.pop(chosen_tile[0])
        chosen_tile[1].num = random.choices([2, 4], [.8, .2])[0]
    
    def reset(self):
        self.reset_tiles()
        self._open_tiles.clear()

    # def up(self, targets:dict[Tuple[int,int], Tile]):
    #     changed = False

    #     for i in range(self.size()-1):
    #         for j in range(self.size()):
    #             tile = self._tiles[i][j]
    #             startig_value = tile.num
    #             k = i+1
    #             tile_under = self._tiles[k][j]
    #             while(collision(tile_under, tile) and k < self.size()-1):
    #                 k += 1
    #                 tile_under = self._tiles[k][j]
    #             if(startig_value != tile.num):
    #                 targets[k, j] = tile
    #             changed |= tile.num != startig_value

    #     self._update_open_tiles
    #     return changed

    def down(self, targets: dict[Tuple[int, int], Tile]):
        changed = False

        for j in range(self.size()):
            i = self.size() - 1

            while (i > 0):
                # tile is destination
                tile = self._tiles[i][j]

                # tile from left is a candidate source
                tile_above = self.get_next_candi_tile((i, j), (0, -1))

                while(tile_above != None):
                    if(tile.num == 0 or tile.num == tile_above.num):
                        # tile from left should move to destination
                        src_x, src_y = self.get_index_from_position(
                            tile_above.x, tile_above.y)
                        targets[(src_x, src_y)] = (i, j)
                        changed = True
                        if(tile.num == 0):
                            tile.num = tile_above.num
                            tile_above.num = 0
                            # switch but keep checking for summation

                        elif(tile.num == tile_above.num):
                            tile.num *= 2
                            tile_above.num = 0
                            if(i == 1):
                                # no need to check another tiles in row since
                                # tile can't be destination and no more destinations
                                # available in this row...
                                break
                            # tile can't be destination anymore but
                            # another tile in row might be.
                            i -= 1
                            tile = self._tiles[i][j]
                    else:
                        if(i == 1):
                            break
                        i -= 1
                        tile = self._tiles[i][j]

                    tile_above = self.get_next_candi_tile((i, j), (0, -1))
                i -= 1
                tile = self._tiles[i][j]

        self._update_open_tiles()
        return changed

    def up(self, targets: dict[Tuple[int, int], Tile]):
        changed = False

        for j in range(self.size()):
            i = 0

            while (i < self.size()-1):
                # tile is destination
                tile = self._tiles[i][j]

                # tile from left is a candidate source
                tile_below = self.get_next_candi_tile((i, j), (0, 1))

                while(tile_below != None):
                    if(tile.num == 0 or tile.num == tile_below.num):
                        # tile from left should move to destination
                        src_x, src_y = self.get_index_from_position(
                            tile_below.x, tile_below.y)
                        targets[(src_x, src_y)] = (i, j)
                        changed = True
                        if(tile.num == 0):
                            tile.num = tile_below.num
                            tile_below.num = 0
                            # switch but keep checking for summation

                        elif(tile.num == tile_below.num):
                            tile.num *= 2
                            tile_below.num = 0
                            if(i == self.size() - 2):
                                # no need to check another tiles in row since
                                # tile can't be destination and no more destinations
                                # available in this row...
                                break
                            # tile can't be destination anymore but
                            # another tile in row might be.
                            i += 1
                            tile = self._tiles[i][j]
                    else:
                        if(i == self.size() - 2):
                            break
                        i += 1
                        tile = self._tiles[i][j]

                    tile_below = self.get_next_candi_tile((i, j), (0, 1))
                i += 1
                tile = self._tiles[i][j]

        self._update_open_tiles()
        return changed

    def left(self, targets: dict[Tuple[int, int], Tile]):
        changed = False

        for i in range(self.size()):
            j = 0

            while (j < self.size()-1):
                # tile is destination
                tile = self._tiles[i][j]

                # tile from left is a candidate source
                tile_from_right = self.get_next_candi_tile((i, j), (1, 0))

                while(tile_from_right != None):
                    if(tile.num == 0 or tile.num == tile_from_right.num):
                        # tile from left should move to destination
                        src_x, src_y = self.get_index_from_position(
                            tile_from_right.x, tile_from_right.y)
                        targets[(src_x, src_y)] = (i, j)
                        changed = True
                        if(tile.num == 0):
                            tile.num = tile_from_right.num
                            tile_from_right.num = 0
                            # switch but keep checking for summation

                        elif(tile.num == tile_from_right.num):
                            tile.num *= 2
                            tile_from_right.num = 0
                            if(j == self.size()-2):
                                # no need to check another tiles in row since
                                # tile can't be destination and no more destinations
                                # available in this row...
                                break
                            # tile can't be destination anymore but
                            # another tile in row might be.
                            j += 1
                            tile = self._tiles[i][j]
                    else:
                        if(j == self.size()-2):
                            break
                        j += 1
                        tile = self._tiles[i][j]

                    tile_from_right = self.get_next_candi_tile((i, j), (1, 0))
                j += 1
                tile = self._tiles[i][j]

        self._update_open_tiles()
        return changed

    def right(self, targets: dict[Tuple[int, int], Tile]):
        changed = False

        for i in range(self.size()):
            j = self.size()-1

            while (j > 0):
                # tile is destination
                tile = self._tiles[i][j]

                # tile from left is a candidate source
                tile_from_left = self.get_next_candi_tile((i, j), (-1, 0))

                while(tile_from_left != None):
                    if(tile.num == 0 or tile.num == tile_from_left.num):
                        # tile from left should move to 
                        # destination
                        src_x, src_y = self.get_index_from_position(
                            tile_from_left.x, tile_from_left.y)
                        targets[(src_x, src_y)] = (i, j)
                        changed = True
                        if(tile.num == 0):
                            tile.num = tile_from_left.num
                            tile_from_left.num = 0
                            # switch but keep checking for summation

                        elif(tile.num == tile_from_left.num):
                            tile.num *= 2
                            tile_from_left.num = 0
                            if(j == 1):
                                # no need to check another tiles in row since
                                # tile can't be destination and no more destinations
                                # available in this row...
                                break
                            # tile can't be destination anymore but
                            # another tile in row might be.
                            j -= 1
                            tile = self._tiles[i][j]
                    else:
                        if(j == 1):
                            break
                        j -= 1
                        tile = self._tiles[i][j]

                    tile_from_left = self.get_next_candi_tile((i, j), (-1, 0))
                j -= 1
                tile = self._tiles[i][j]

        self._update_open_tiles()
        return changed

    def game_over_check(self):
        if(len(self._open_tiles) > 0):
            return False
        for i in range(self.size()):
            for j in range(self.size()):
                tile = self._tiles[i][j]
                if(j < self.size()-1 and tile.num == self._tiles[i][j+1].num):
                    return False
                if(i < self.size()-1 and tile.num == self._tiles[i+1][j].num):
                    return False
        return True

    def get_initial_position(self, i, j):
        return (self.x + j*self.tile_size, self.y + i * self.tile_size)

    def get_index_from_position(self, x, y):
        return ((y-self.y)//self.tile_size, (x-self.x)//self.tile_size)

    def get_next_candi_tile(self, cordinates: tuple[int, int], direction: tuple[int, int]):
        i, j = cordinates
        j_shift, i_shift = direction
        res = None
        while(0 <= i + i_shift < self.size() and 0 <= j + j_shift < self.size()):
            i += i_shift
            j += j_shift
            res = self._tiles[i][j]
            if(res.num != 0):
                return res
        return None


def collision(src: Tile, dst: Tile):
    res = src.num == 0
    if(dst.num == 0):
        dst.num = src.num
        src.num = 0
        return True
    elif(dst.num == src.num):
        dst.num *= 2
        src.num = 0
        return False
    return res
