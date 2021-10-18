from pygame import mixer

mixer.init()
mixer.music.set_volume(1)

UNDERTALE = mixer.Sound("sounds/undertale.wav")

SHATTER_1 = mixer.Sound("sounds/Glass Shatter 1.wav")
SHATTER_2 = mixer.Sound("sounds/Glass Shatter 2.wav")
SHATTER_3 = mixer.Sound("sounds/Glass Shatter 3.wav")

class SoundPlayer:
    def __init__(self):
        pass

    def play(self, sound):
        sound.play()
