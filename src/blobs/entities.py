import pyglet
from .sprite import GameSprite
from . import graphics
from . import sound
from .sound import playsound
from random import choice, randint, randrange
from math import hypot

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


class SubBullet(GameSprite):
    def __init__(self, *a, **ka):
        self.parent = ka.pop("parent")
        super().__init__(*a, **ka)

    def act(self, game):
        if not self.parent.visible:
            return

        self.clear_cell(game.cells)

        self.fx = self._x + self._vec[0]
        self.fy = self._y + self._vec[1]

        collider = None
        if self.grid_collide(game.grid):
            self.fx += (self._vec[0] > 0) * 2
            self.fy += (self._vec[1] > 0) * 2

            game.sprites.append(
                Splat(
                    img=Bullet.img2,
                    x=self.fx,
                    y=self.fy,
                    batch=game.window.foreground,
                )
            )
            collider = True

        elif collider := self.collide(game.cells):
            if isinstance(collider, Enemy):
                collider.die(game)

        if collider:
            self.fx = self._x
            self.fy = self._y
            self.visible = False
            self.parent.visible = None
        else:
            self._x = self.fx
            self.y = self.fy
            self.add_cell(game.cells)


class Splat(GameSprite):
    def __init__(self, *a, **ka):
        super().__init__(*a, **ka)
        self.timer = 60

    def act(self, game):
        self.timer -= 1
        if not self.timer:
            self.visible = False


class Bullet:
    img = (
        pyglet.image.SolidColorImagePattern((0, 253, 0, 255))
        .create_image(2, 2)
        .get_texture()
    )
    img2 = (
        pyglet.image.SolidColorImagePattern((255, 0, 0, 255))
        .create_image(2, 2)
        .get_texture()
    )

    # TODO: reuse bullets instead of recreating

    def __init__(self, game):
        player = game.player
        window = game.window

        x = player.x + player.w // 2
        y = player.y + player.h // 2

        self.bullets = []
        self.visible = True

        for _ in range(10):
            b = SubBullet(
                img=Bullet.img2 if _ == 9 else Bullet.img,
                x=x,
                y=y,
                batch=window.foreground,
                parent=self,
            )

            self.bullets.append(b)
            x += player.shot_vector[0] * 2
            y += player.shot_vector[1] * 2
            b._vec = [n * 10 for n in player.shot_vector]

            collider = None

            if b.grid_collide(game.grid):
                b.fx += (b._vec[0] > 0) * 2
                b.fy += (b._vec[1] > 0) * 2

                game.sprites.append(
                    Splat(
                        img=Bullet.img2,
                        x=b.fx,
                        y=b.fy,
                        batch=game.window.foreground,
                    )
                )
                collider = True

            elif collider := b.collide(game.cells):
                collider.die(game)

            if collider:
                b.visible = False
                self.visible = False
                break

            b.add_cell(game.cells)

        player.shot_timer = [7 if n else 0 for n in player.shot_vector]
        game.sprites.extend(self.bullets)

    def event(self, game):
        if not self.visible:
            for b in self.bullets:
                b.visible = False
                try:
                    b.clear_cell(game.cells)
                except KeyError:
                    ...

            self.bullets = []


class Player(GameSprite):
    def __init__(self, game):
        window = game.window
        super().__init__(img=graphics.humanoid[0], batch=window.foreground)
        self._vec = [0, 0]
        self._x = 24
        self.y = 24
        self.fx = self._x
        self.fy = self._y
        self.speed = 2
        self.anim = 0
        self.shot_vector = [0, 0]
        self.shot_timer = [0, 0]
        self.add_cell(game.cells)
        game.sprites.append(self)

    def act(self, game):
        window = game.window

        if game.bullets:
            for bullet in game.bullets:
                bullet.event(game)
            game.bullets = [b for b in game.bullets if b.bullets]

        self.shot_timer = [n - 1 if n else n for n in self.shot_timer]

        if any(self.shot_vector) and not any(self.shot_timer):
            playsound(sound.shot)
            game.bullets.append(Bullet(game))

        if any(self._vec):
            self.clear_cell(game.cells)

            anim = 3
            if self._vec[1]:
                anim = (3, 2)[self._vec[1] > 0]
            if self._vec[0]:
                anim = (0, 1)[self._vec[0] > 0]

            if not self.anim % 4:
                self._set_texture(graphics.humanoid[(anim, self.anim // 4)])

            self.anim = (self.anim + 1) % 16

            self.fx = self._x + self._vec[0]
            if self.grid_collide(game.grid):
                self.fx = self._x

            self.fy = self._y + self._vec[1]
            if self.grid_collide(game.grid):
                self.fy = self._y

            if self.collide(game.cells):
                self.fx = self._x
                self.fy = self._y
            else:
                self._x = self.fx
                self.y = self.fy

            self.add_cell(game.cells)


class Enemy(GameSprite):
    def __init__(self, game):
        window = game.window
        anim = choice(animations)
        a_pos = randrange(len(anim))

        super().__init__(img=graphics.anim[anim[a_pos]], batch=window.batch)

        self.mode = 0
        self._anim = anim
        self._a_pos = a_pos
        self._vec = [0, 0]
        self.timer = randint(0, 50)
        self.speed = randint(1, 3)
        game.sprites.append(self)

    def place(self, game):
        while True:
            x1, x2, y1, y2 = choice(game.safe_zones)
            self._x = randint(x1, x2 - self.w)
            self._y = randint(y1, y2 - self.h)
            self.fx = self._x
            self.fy = self._y
            self.add_cell(game.cells)
            if not self.grid_collide(game.grid) and not self.collide(game.cells):
                break
            self.clear_cell(game.cells)

        self.x = self._x
        self._vec = [n * self.speed for n in choice(vecs)]

    def act(self, game):
        self.timer = (self.timer + 1) % 50

        if not self.timer % 2:
            return

        dx = game.player.x - self._x
        dy = game.player.y - self._y
        dist = hypot(dx, dy)

        if self.timer == 1:
            if self.mode == 1:
                if dist > 100 or randint(1, 4) == 3:
                    self.mode == 0
                    self._vec = choice(vecs)
                    self.speed = randint(1, 4)
        else:
            if dist < 100:
                self.mode == 1
                dx, dy = dx / dist, dy / dist
                self.speed = 4
                self._vec = [int(dx * self.speed), int(dy * self.speed)]

        if self.timer % 10 == 1:
            self._a_pos = (self._a_pos + 1) % len(self._anim)
        self._set_texture(graphics.anim[self._anim[self._a_pos]])

        self.clear_cell(game.cells)

        self.fx = self._x + self._vec[0]
        if self.grid_collide(game.grid):
            self.fx = self._x
            self.speed = randint(1, 4)
            self._vec = [n * self.speed for n in choice(vecs)]

        self.fy = self._y + self._vec[1]
        if self.grid_collide(game.grid):
            self.fy = self._y
            self.speed = randint(1, 4)
            self._vec = [n * self.speed for n in choice(vecs)]

        if collider := self.collide(game.cells):
            if isinstance(collider, SubBullet):
                self.die(game)
                return
            self.fx = self._x
            self.fy = self._y
            self.mode = 0
            self.speed = randint(1, 4)
            self._vec = [n * self.speed for n in choice(vecs)]
        else:
            self._x = self.fx
            self.y = self.fy

        self.add_cell(game.cells)

    def die(self, game):
        playsound(choice(sound.explosions))
        self.__class__ = Dead
        self.reset(game)


class Dead(GameSprite):
    def reset(self, game):
        self.timer = 60
        self.image = graphics.dead[19]

    def act(self, game):
        self.timer -= 1
        if self.timer>52:            
            self.image = graphics.dead[
                ((self.timer) % 4) + 16
            ]
        elif self.timer == 52:
            self.image = graphics.dead[randint(0,15)]
        if not self.timer:
            self.visible = False
            self.clear_cell(game.cells)


GameSprite.collisions = set()
SubBullet.collisions = {Enemy}
Player.collisions = {Enemy}
Enemy.collisions = {Player, Enemy, Dead}
