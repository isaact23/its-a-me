from pygame import mixer

mixer.init()
mixer.music.set_volume(1)
UNDERTALE = mixer.Sound("sounds/undertale.wav")


class SoundPlayer:
    def __init__(self):
        pass

    def play(self, sound):
        sound.play()
