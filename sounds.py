import random
from pygame import mixer

mixer.init()
mixer.music.set_volume(1)

UNDERTALE = mixer.Sound("sounds/Undertale.ogg")

SHATTER_1 = mixer.Sound("sounds/Glass Shatter 1.ogg")
SHATTER_2 = mixer.Sound("sounds/Glass Shatter 2.ogg")
SHATTER_3 = mixer.Sound("sounds/Glass Shatter 3.ogg")

FINAL_FANTASY = mixer.Sound("sounds/Final Fantasy VII - One Winged Angel.ogg")


class SoundPlayer:
    def __init__(self):
        pass

    def play(self, sound):
        """
        :param sound: The Sound object to play.
        """
        sound.play()

    def shatter(self):
        """
        Play a random glass shattering sound.
        """
        self.play(random.choice([SHATTER_1, SHATTER_2, SHATTER_3]))

    def stop(self):
        mixer.stop()
