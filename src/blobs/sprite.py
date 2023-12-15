import pyglet
from .constants import *


class GameSprite(pyglet.sprite.Sprite):
    def __init__(self, *a, **ka):
        super().__init__(*a, **ka)
        self.w = self.width
        self.h = self.height
        self.fx = self._x
        self.fy = self._y
        self.cells = set()

    def add_cell(self, cells):
        """
        Add this sprite to all the cells in the collision detection grid
        that it is big enough to cover.
        """
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
        """
        Remove this sprite from all the cells in the collision detection grid
        that it currently occupies.
        """
        for cell in self.cells:
            cells[cell].remove(self)
        self.cells.clear()

    def collide(self, cells):
        """
        Test this sprite for collisions with all other elements,
        based on the sprite's fx/fy coordinates (its prospective move).
        We don't need to have an element in any cells to test collisions,
        so this allows us to speed up our tests slightly, and to test
        in a more granular way.
        """

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
        """
        Test if the sprite collides with an element in the maze grid.
        """
        csx = self.fx // GRID_SIZE
        csy = ((self.fx + self.w) // GRID_SIZE) + 1
        xx = range(csx, csy)
        for y in range(self.fy // GRID_SIZE, ((self.fy + self.h) // GRID_SIZE) + 1):
            for x in xx:
                if grid[(x, y)]:
                    return True

    def oob(self):
        """
        Test if the sprite has gone offscreen.
        """
        return (
            self.fx < 0
            or self.fx + self.w > WIDTH
            or self.fy < 0
            or self.fy + self.h > HEIGHT
        )
