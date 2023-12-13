from random import choice
import pyglet

from .constants import *
from .entities import Enemy, Player
import array


class Grid(array.array):
    __slots__ = "_width", "_height", "cache", "grid_texture", "grid_sprite"
    post = array.array("B", b"\x00\x40\xff\xff")
    spacing = 8
    positions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __new__(cls, width, height):
        item = super().__new__(cls, "B", b"\x00" * (width * height * 4))
        item._width = width
        item._height = height
        item.cache = {}
        return item

    def generate_maze(self):
        for _ in range(GRID_WIDTH):
            self[(_, 0)] = Grid.post
            self[(_, GRID_HEIGHT - 1)] = Grid.post
        for _ in range(GRID_HEIGHT):
            self[(0, _)] = Grid.post
            self[(GRID_WIDTH - 1, _)] = Grid.post

        for x in range(Grid.spacing, GRID_WIDTH, Grid.spacing):
            for y in range(Grid.spacing, GRID_HEIGHT, Grid.spacing):
                vx, vy = choice(Grid.positions[:2])
                x1 = x
                y1 = y
                for _ in range(Grid.spacing):
                    self[(x1, y1)] = Grid.post
                    x1 += vx
                    y1 += vy
                Grid.positions.insert(0, Grid.positions.pop())

    def create_sprite(self, window):
        self.grid_texture = pyglet.image.Texture.create(
            WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
        )
        self.update_sprite()
        self.grid_sprite = pyglet.sprite.Sprite(
            img=self.grid_texture,
            batch=window.foreground,
        )
        self.grid_sprite.scale = GRID_SIZE

    def update_sprite(self):
        self.grid_texture.blit_into(
            pyglet.image.ImageData(
                WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE, "RGBA", self.tobytes()
            ),
            0,
            0,
            0,
        )

    def __getitem__(self, idx):
        return self.cache.get(idx, None)

    def __setitem__(self, idx, val):
        self.cache[idx] = val
        x, y = idx
        pos = ((y % self._height) * self._width + (x % self._width)) * 4
        return super().__setitem__(slice(pos, pos + 4), val)


class Game:
    __slots__ = "window", "sprites", "bullets", "cells", "grid", "safe_zones", "player"

    def __init__(self, window):
        self.window = window
        self.sprites = []
        self.bullets = []
        self.cells = {}
        self.grid = Grid(GRID_WIDTH, GRID_HEIGHT)

    def new_game(self):
        window = self.window
        self.grid.generate_maze()
        self.grid.create_sprite(window)

        for y in range(-1, HEIGHT // CELL_SIZE + 2):
            for x in range(-1, WIDTH // CELL_SIZE + 2):
                self.cells[(x, y)] = set()

        self.safe_zones = (
            (128, WIDTH, 0, HEIGHT),
            (0, WIDTH, 128, HEIGHT),
        )

        self.player = Player(self)

        for _ in range(200):
            sprite = Enemy(self)
            sprite.place(self)
