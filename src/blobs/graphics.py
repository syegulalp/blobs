import pyglet


def make_resource(name, x, y):
    res = pyglet.resource.image(name)
    return pyglet.image.TextureGrid(pyglet.image.ImageGrid(res, x, y))


# TODO: extract blast to its own sheet for easier working

anim = make_resource("Blobbo.png", 6, 5)
dead = make_resource("Dead.png", 5, 4)
humanoid = make_resource("Humanoid.png", 4, 4)
