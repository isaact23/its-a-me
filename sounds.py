import enum, pathlib, pyaudio, random

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


class SoundPlayer:
    def __init__(self):
        self.mode = self.Mode.NONE

    # All possible states for the sound player to be in.
    class Mode(enum.Enum):
        NONE = 0
        ATTRACT = 1
    
    # Update loop. Restart songs if necessary
    def update(self):
        if self.mode == self.Mode.ATTRACT:
            pass
            # Play attract music if not already playing

    # Update mode.
    def set_mode(self, mode):
        if mode != self.mode:
            # Stop all music
            self.mode = mode

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
