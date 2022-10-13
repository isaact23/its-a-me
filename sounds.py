import enum, pathlib, random
from pygame import mixer

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

mixer.init(44100, -16, 1, 1024)
mixer.music.set_volume(0.1)

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
            if not mixer.music.get_busy():
                self.play_music(random.choice(ATTRACT_MUSIC))

    # Update mode.
    def set_mode(self, mode):
        if mode != self.mode:
            # Stop all music
            self.mode = mode

    # Play a music file.
    def play_music(self, music):
        try:
            mixer.Sound(music).play()
            print("Played music", music)
        except FileNotFoundError:
            print("Error playing music", music)
        
    # Play a sound file.
    def play_sound(self, sound):
        pass
