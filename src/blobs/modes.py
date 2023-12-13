class Loop:
    def __init__(self, window, game):
        self.window = window
        self.game = game


class MainLoop(Loop):
    def event(self, *a):
        game = self.game
        window = self.window

        with window.timer:
            game.sprites = [s for s in game.sprites if s._visible]
            for sprite in game.sprites:
                sprite.act(game)

    def on_draw(self, *a, **ka):
        window = self.window
        self.event()
        window.clear()
        window.batch.draw()
        window.foreground.draw()

    # theoretically we could move this to the player object

    def on_key_press(self, symbol, modifiers):
        p = self.game.player
        print(symbol)

        if symbol == 97:
            p.shot_vector[0] -= 1
        elif symbol == 100:
            p.shot_vector[0] += 1
        if symbol == 119:
            p.shot_vector[1] += 1
        elif symbol == 115:
            p.shot_vector[1] -= 1

        if symbol == 65361:
            p._vec[0] -= p.speed
            p.anim = 0
        elif symbol == 65363:
            p._vec[0] += p.speed
            p.anim = 0

        if symbol == 65364:
            p._vec[1] -= p.speed
            p.anim = 0
        elif symbol == 65362:
            p._vec[1] += p.speed
            p.anim = 0

    def on_key_release(self, symbol, modifiers):
        p = self.game.player
        if symbol == 97:
            p.shot_vector[0] += 1
        elif symbol == 100:
            p.shot_vector[0] -= 1
        if symbol == 119:
            p.shot_vector[1] -= 1
        elif symbol == 115:
            p.shot_vector[1] += 1

        if symbol == 65361:
            p._vec[0] += p.speed
            p.anim = 0
        elif symbol == 65363:
            p._vec[0] -= p.speed
            p.anim = 0
        if symbol == 65364:
            p._vec[1] += p.speed
            p.anim = 0
        elif symbol == 65362:
            p._vec[1] -= p.speed
            p.anim = 0
