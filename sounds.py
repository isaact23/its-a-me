import pathlib
import random

import pygame
from pygame import mixer

ENABLE_SOUND = True

SOUND_DIR = pathlib.Path(__file__).parent / 'sounds'


# Import sounds from directories
def get_sounds_from(dir):
    """
    Return all sounds from a given subdirectory of sounds.
    :param dir: The directory to retrive sounds from.
    :return: An array of paths to sound files.
    """
    return [str(s) for s in (SOUND_DIR / dir).iterdir()]


ATTRACT_MUSIC = get_sounds_from('attract_music')
CHOOSE_MUSIC = get_sounds_from('choose_music')
CORRECT_SOUNDS = get_sounds_from('correct')
WRONG_SOUNDS = get_sounds_from('wrong')
SCREAM_SOUNDS = get_sounds_from('screams')
SCARY_SCREAM_SOUNDS = get_sounds_from('screams_scary')
WIN_MUSIC = get_sounds_from('win_music')

UNDERTALE = "sounds/misc/Undertale.ogg"
GLRL_ONCE = "sounds/misc/Squid Game - Green Light Red Light Once.ogg"

CHOOSE_MUSIC_TEMPOS = (120, 132, 160, 184, 150, 148)

if ENABLE_SOUND:
    mixer.init(44100, -16, 1, 1024)
    mixer.music.set_volume(0.1)


class SoundPlayer:
    def __init__(self, kid_mode):
        """
        :param kid_mode: Set to True to omit scary sounds.
        """
        self.kid_mode = kid_mode

    def attract_music(self):
        # TODO: Loop different music tracks
        if ENABLE_SOUND:
            self.music(random.choice(ATTRACT_MUSIC), 1)

    def choose_music(self):
        """
        Play a random track from choose_music.
        :return: The tempo of the thinking music.
        """
        index = random.randint(0, len(CHOOSE_MUSIC) - 1)
        self.music(CHOOSE_MUSIC[index], -1)
        tempo = CHOOSE_MUSIC_TEMPOS[index]
        print("Tempo of choose music is", tempo)
        return tempo

    def music(self, sound, loops):
        """
        Loop the sound indefinitely.
        :param sound: The sound to loop as music.
        :param loops: The number of times to loop the track. -1 for unlimited.
        """
        try:
            mixer.music.load(sound)
            mixer.music.play(loops)
            print("Playing music", sound)
        except pygame.error:
            print("Error playing music", sound)

    def play(self, sound):
        """
        :param sound: The Sound object to play.
        """
        try:
            mixer.Sound(sound).play()
            print("Played sound", sound)
        except FileNotFoundError:
            print("Error playing sound", sound)

    def correct(self):
        """
        Play a random 'correct' sound.
        """
        self.play(random.choice(CORRECT_SOUNDS))

    def wrong(self):
        """
        Play a random 'wrong' sound upon the player stepping on the wrong tile.
        """
        self.play(random.choice(WRONG_SOUNDS))

    def scream(self):
        """
        Play a random screaming sound.
        """
        if self.kid_mode:
            self.play(random.choice(SCREAM_SOUNDS))
        else:
            self.play(random.choice(SCARY_SCREAM_SOUNDS + SCREAM_SOUNDS))

    def win(self):
        """
        Play a random win fanfare.
        """
        self.play(random.choice(WIN_MUSIC))

    def stop(self):
        """
        Stop all sounds.
        """
        mixer.stop()
        mixer.music.stop()

    def get_busy(self):
        """
        Return true if music is playing.
        """
        return mixer.music.get_busy()
