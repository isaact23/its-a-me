import pathlib
import random

import pygame
from pygame import mixer

KID_MODE = True

SOUND_DIR = pathlib.Path(__file__).parent / 'sounds'

# Import sounds from directories
ATTRACT_MUSIC = [str(s) for s in (SOUND_DIR / 'attract_music').iterdir()]
CORRECT_SOUNDS = [str(s) for s in (SOUND_DIR / 'correct').iterdir()]
WRONG_SOUNDS = [str(s) for s in (SOUND_DIR / 'wrong').iterdir()]
SCREAM_SOUNDS = [str(s) for s in (SOUND_DIR / 'screams').iterdir()]
SCARY_SCREAM_SOUNDS = [str(s) for s in (SOUND_DIR / 'screams_scary').iterdir()]

UNDERTALE = "sounds/Undertale.ogg"

CHOOSE_MUSIC = ["sounds/choose_music/Jeopardy.ogg",
                "sounds/choose_music/Final Fantasy VII - One Winged Angel.ogg",
                "sounds/choose_music/Undertale OST - 007 - Anticipation.ogg",
                "sounds/choose_music/Undertale OST - 016 - Nyeh Heh Heh!.ogg",
                "sounds/choose_music/Paper Mario - Koopa Bros Battle Music.ogg"]
CHOOSE_MUSIC_TEMPOS = (132, 120, 184, 150, 158)

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
        try:
            mixer.music.load(sound)
            mixer.music.play(-1)
        except pygame.error:
            print("Error playing music", sound)

    def play(self, sound):
        """
        :param sound: The Sound object to play.
        """
        try:
            mixer.Sound(sound).play()
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
        if KID_MODE:
            self.play(random.choice(SCREAM_SOUNDS))
        else:
            self.play(random.choice(SCARY_SCREAM_SOUNDS + SCREAM_SOUNDS))

    def win(self):
        """
        Play a random win fanfare.
        """
        self.play(WIN_MUSIC_1)

    def stop(self):
        mixer.stop()
        mixer.music.stop()
