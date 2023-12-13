import pyglet
from .constants import *

animations = (
    (0, 1, 2, 9),
    (3, 4),
    (5, 6),
    (7, 8, 25, 8),
    (12,),
    (13, 14),
    (16, 17, 18, 19, 10, 11),
    (28, 29, 20, 21, 22, 23),
    (24,),
    (25,),
    (26, 25, 27, 25),
)

vecs = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


class GameSprite(pyglet.sprite.Sprite):
    def __init__(self, *a, **ka):
        super().__init__(*a, **ka)
        self.w = self.width
        self.h = self.height
        self.fx = self._x
        self.fy = self._y
        self.cells = set()

    def add_cell(self, cells):
        wt = self.fx + self.w
        csx = self.fx // CELL_SIZE
        csy = (wt // CELL_SIZE) + 1

        xx = range(csx, csy)
        for y in range(self.fy // CELL_SIZE, ((self.fy + self.h) // CELL_SIZE) + 1):
            for x in xx:
                pos = (x, y)
                cells[pos].add(self)
                self.cells.add(pos)

    def clear_cell(self, cells):
        for cell in self.cells:
            cells[cell].remove(self)
        self.cells.clear()

    def collide(self, cells):
        other: GameSprite

        wt = self.fx + self.w
        ht = self.fy + self.h
        csx = self.fx // CELL_SIZE
        csy = (wt // CELL_SIZE) + 1

        xx = range(csx, csy)
        for y in range(self.fy // CELL_SIZE, (ht // CELL_SIZE) + 1):
            for x in xx:
                for other in cells[(x, y)]:
                    if (
                        other is not self
                        and other.__class__ in self.collisions
                        and ht >= other.fy
                        and wt >= other.fx
                        and other.fx + other.w >= self.fx
                        and other.fy + other.h >= self.fy
                    ):
                        return other

    def grid_collide(self, grid):
        csx = self.fx // GRID_SIZE
        csy = ((self.fx + self.w) // GRID_SIZE) + 1
        xx = range(csx, csy)
        for y in range(self.fy // GRID_SIZE, ((self.fy + self.h) // GRID_SIZE) + 1):
            for x in xx:
                if grid[(x, y)]:
                    return True

    def oob(self):
        if (
            self.fx < 0
            or self.fx + self.w > WIDTH
            or self.fy < 0
            or self.fy + self.h > HEIGHT
        ):
            return True
