import pathlib, random
from pygame import mixer

KID_MODE = True

SOUND_DIR = pathlib.Path(__file__).parent / 'sounds'

ATTRACT_MUSIC = [str(s) for s in (SOUND_DIR / 'attract_music').iterdir()]
SHATTER_SOUNDS = [str(s) for s in (SOUND_DIR / 'shatters').iterdir()]
SCREAM_SOUNDS = [str(s) for s in (SOUND_DIR / 'screams').iterdir()]

UNDERTALE = "sounds/Undertale.ogg"

CORRECT_1 = "sounds/Super Mario World - Correct.ogg"

CHOOSE_MUSIC_1 = "sounds/choose_music/Jeopardy"
CHOOSE_MUSIC_2 = "sounds/choose_music/Final Fantasy VII - One Winged Angel.ogg"

WIN_MUSIC_1 = "sounds/win_music/Super Mario Bros Course Clear.ogg"

mixer.init(10000, -16, 1, 1024)
mixer.music.set_volume(0.1)


class SoundPlayer:
    def __init__(self):
        pass

    def attract_music(self):
        # TODO: Loop different music tracks
        self.music(random.choice(ATTRACT_MUSIC))

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
