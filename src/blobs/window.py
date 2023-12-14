import pyglet

from .constants import *


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(visible=False, width=WIDTH * ZOOM, height=HEIGHT * ZOOM)
        self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_WAIT_ARROW))

        self.set_location(
            self.screen.width // 2 - self.width // 2,
            self.screen.height // 2 - self.height // 2,
        )

        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.Batch()
        self.foreground = pyglet.graphics.Batch()

        self.mode = None
        self.mode_stack = []

        from .game import Game
        from .modes import MainLoop

        self.game = Game(self)
        self.game.new_game()

        self.push_mode(MainLoop)

        self.view = self.view.scale((ZOOM, ZOOM, 1))
        self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_DEFAULT))
        self.set_visible(True)

    def push_mode(self, mode):
        if self.mode:
            self.mode_stack.append(self.mode)
        self.mode = mode(self, self.game)
        self.set_mode_bindings()
        self.mode.enter()

    def pop_mode(self):
        self.mode.exit()
        self.mode = self.mode_stack.pop()
        self.set_mode_bindings()

    def set_mode_bindings(self):
        for m in ("on_key_press", "on_key_release", "on_draw"):
            setattr(self, f"_{m}", getattr(self.mode, m))

    def on_key_press(self, *a, **ka):
        return self._on_key_press(*a, **ka)

    def on_key_release(self, *a, **ka):
        return self._on_key_release(*a, **ka)

    def on_draw(self, *a, **ka):
        return self._on_draw(*a, **ka)
