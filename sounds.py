import random
from pygame import mixer

mixer.init()
mixer.music.set_volume(1)

UNDERTALE = mixer.Sound("sounds/Undertale.ogg")

CORRECT_1 = mixer.Sound("sounds/Super Mario World - Correct.ogg")

SHATTER_1 = mixer.Sound("sounds/Glass Shatter 1.ogg")
SHATTER_2 = mixer.Sound("sounds/Glass Shatter 2.ogg")
SHATTER_3 = mixer.Sound("sounds/Glass Shatter 3.ogg")

SCREAM_1 = mixer.Sound("sounds/Scream - Goat.ogg")
SCREAM_2 = mixer.Sound("sounds/Scream - Neverhood.ogg")
SCREAM_3 = mixer.Sound("sounds/Scream - Mr Bile.ogg")

FINAL_FANTASY = mixer.Sound("sounds/Final Fantasy VII - One Winged Angel.ogg")


class SoundPlayer:
    def __init__(self):
        pass

    def play(self, sound):
        """
        :param sound: The Sound object to play.
        """
        sound.play()

    def correct(self):
        """
        Play a random 'correct' sound.
        """
        self.play(CORRECT_1)

    def shatter(self):
        """
        Play a random glass shattering sound.
        """
        self.play(random.choice([SHATTER_1, SHATTER_2, SHATTER_3]))

    def scream(self):
        """
        Play a random screaming sound.
        """
        self.play(random.choice([SCREAM_1, SCREAM_2, SCREAM_3]))

    def stop(self):
        mixer.stop()
