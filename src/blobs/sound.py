import pyglet

audio = pyglet.media.Player()
shot = pyglet.resource.media("shot.wav", streaming=False)
explosions = tuple(
    pyglet.resource.media(f"explosion{n}.wav", streaming=False) for n in range(1, 4)
)


def playsound(sound):
    if audio.playing:
        audio.pause()
        audio.queue(sound)
        audio.next_source()
    else:
        audio.queue(sound)
    audio.play()

# This is done to prime the audio player,
# and prevent discernible lag on first play of game sounds.

audio.volume = 0
playsound(shot)
audio.pause()
audio.next_source()
audio.volume = 1