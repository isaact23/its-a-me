import random
from pygame import mixer

mixer.init()
mixer.music.set_volume(1)

AMBIENT_MUSIC_1 = "sounds/Ambient Horror Music - Red Space.ogg"

UNDERTALE = "sounds/Undertale.ogg"

CORRECT_1 = "sounds/Super Mario World - Correct.ogg"

SHATTER_1 = "sounds/Glass Shatter 1.ogg"
SHATTER_2 = "sounds/Glass Shatter 2.ogg"
SHATTER_3 = "sounds/Glass Shatter 3.ogg"

SCREAM_1 = "sounds/Scream - Goat.ogg"
SCREAM_2 = "sounds/Neverhood - Fall Scream.ogg"
SCREAM_3 = "sounds/Monsters Inc - Mr Bile Scream.ogg"
SCREAM_4 = "sounds/Homer Simpson Scream.ogg"
SCREAM_5 = "sounds/Spongebob My Leg.ogg"

FINAL_FANTASY = "sounds/Final Fantasy VII - One Winged Angel.ogg"

WIN_MUSIC_1 = "sounds/Super Mario Bros Course Clear.ogg"


class SoundPlayer:
    def __init__(self):
        pass

    def music(self, sound):
        """
        Loop the sound indefinitely.
        :param sound: The sound to loop as music.
        """
        mixer.music.load(sound)
        mixer.music.play(-1)

    def play(self, sound):
        """
        :param sound: The Sound object to play.
        """
        mixer.Sound(sound).play()

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
        self.play(random.choice([SCREAM_1, SCREAM_2, SCREAM_3, SCREAM_4, SCREAM_5]))

    def win(self):
        """
        Play a random win fanfare.
        """
        self.play(WIN_MUSIC_1)

    def stop(self):
        mixer.stop()
        mixer.music.stop()
