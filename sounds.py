import pathlib
import random

from pygame import mixer

KID_MODE = False

SOUND_DIR = pathlib.Path(__file__).parent / 'sounds'

# Import sounds from directories
ATTRACT_MUSIC = [str(s) for s in (SOUND_DIR / 'attract_music').iterdir()]
CORRECT_SOUNDS = [str(s) for s in (SOUND_DIR / 'correct').iterdir()]
SHATTER_SOUNDS = [str(s) for s in (SOUND_DIR / 'shatters').iterdir()]
SCREAM_SOUNDS = [str(s) for s in (SOUND_DIR / 'screams').iterdir()]

UNDERTALE = "sounds/Undertale.ogg"

CHOOSE_MUSIC = ["sounds/choose_music/Jeopardy.ogg",
                "sounds/choose_music/Final Fantasy VII - One Winged Angel.ogg",
                "sounds/choose_music/Undertale OST - 007 - Anticipation.ogg",
                "sounds/choose_music/Undertale OST - 016 - Nyeh Heh Heh!.ogg"]
CHOOSE_MUSIC_TEMPOS = (132, 120, 184, 150)

WIN_MUSIC_1 = "sounds/win_music/Super Mario Bros Course Clear.ogg"

mixer.init(10000, -16, 1, 1024)
mixer.music.set_volume(0.1)


class SoundPlayer:
    def __init__(self):
        pass

    def attract_music(self):
        # TODO: Loop different music tracks
        self.music(random.choice(ATTRACT_MUSIC))

    def choose_music(self):
        """
        Play a random track from choose_music.
        :return: The tempo of the thinking music.
        """
        index = random.randint(0, len(CHOOSE_MUSIC) - 1)
        self.music(CHOOSE_MUSIC[index])
        return CHOOSE_MUSIC_TEMPOS[index]

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
        self.play(random.choice(CORRECT_SOUNDS))

    def shatter(self):
        """
        Play a random glass shattering sound.
        """
        self.play(random.choice(SHATTER_SOUNDS))

    def scream(self):
        """
        Play a random screaming sound.
        """
        if not KID_MODE:
            self.play(random.choice(SCREAM_SOUNDS))

    def win(self):
        """
        Play a random win fanfare.
        """
        self.play(WIN_MUSIC_1)

    def stop(self):
        mixer.stop()
        mixer.music.stop()
