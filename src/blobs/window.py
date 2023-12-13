import pyglet

from .timer import Timer
from .constants import *


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(visible=False, width=WIDTH * ZOOM, height=HEIGHT * ZOOM)
        self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_WAIT_ARROW))

        self.set_location(
            self.screen.width // 2 - self.width // 2,
            self.screen.height // 2 - self.height // 2,
        )

        self.timer = Timer()
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.Batch()
        self.foreground = pyglet.graphics.Batch()

        from .game import Game
        from .modes import MainLoop

        self.game = Game(self)
        self.game.new_game()

        self.set_mode(MainLoop)

        self.view = self.view.scale((ZOOM, ZOOM, 1))
        self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_DEFAULT))
        self.set_visible(True)

    def set_mode(self, mode):
        self.mode = mode(self, self.game)
        for m in ("on_key_press", "on_key_release", "on_draw"):
            setattr(self, f"_{m}", getattr(self.mode, m))

    def on_key_press(self, *a, **ka):
        return self._on_key_press(*a, **ka)

    def on_key_release(self, *a, **ka):
        return self._on_key_release(*a, **ka)

    def on_draw(self, *a, **ka):
        return self._on_draw(*a, **ka)

    def output(self, *a):
        print("Loop time", self.timer.avg, "%", self.timer.avg / (1 / 60) * 100)
