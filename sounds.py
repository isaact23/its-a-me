import enum, pathlib, random
from pygame import mixer

SOUND_DIR = pathlib.Path(__file__).parent / 'media/sounds'


class SoundPlayer:
    def __init__(self):
        self.mode = self.Mode.NONE
        self.attract_music = self._get_sounds_from('music/attract_music')
        self.tutorial_music = self._get_sounds_from('music/tutorial_music')
        self.play_music = self._get_sounds_from('music/play_music')

        # Initialize pygame sound mixer
        mixer.init(44100, -16, 1, 1024)
        mixer.music.set_volume(1)

    # All possible states for the sound player to be in.
    class Mode(enum.Enum):
        NONE = 0
        ATTRACT = 1
        TUTORIAL = 2
        PLAY = 3
        STINGER = 10  # Used for specific oneshot music tracks

    class Stingers:
        SMG_POWERUP = SOUND_DIR / 'music/stingers/Super Mario Galaxy - Power Up Found.ogg'

    # Update loop. Restart songs if necessary
    def update(self):
        if not mixer.music.get_busy():
            if self.mode == self.Mode.ATTRACT:
                self._play_music(random.choice(self.attract_music))
            elif self.mode == self.Mode.TUTORIAL:
                self._play_music(random.choice(self.tutorial_music))
            elif self.mode == self.Mode.PLAY:
                self._play_music(random.choice(self.play_music))
            elif self.mode == self.Mode.STINGER:
                pass

    # Update mode.
    def set_mode(self, mode, song=None):
        if mode != self.mode:
            self.stop()
            self.mode = mode
            if mode == self.Mode.STINGER:
                self._play_music(song)


    # Stop music.
    def stop(self):
        mixer.music.stop()

    # Play a music file.            if not mixer.music.get_busy():
    def _play_music(self, music):
        try:
            mixer.music.load(music)
            mixer.music.play()
            print("Played music", music)
        except Exception:
            print("Error playing music", music)

    # Play a sound file.
    def _play_sound(self, sound):
        pass

    # Import sounds from directories
    def _get_sounds_from(self, dir):
        """
        Return all sounds from a given subdirectory of sounds.
        :param dir: The directory to retrive sounds from.
        :return: An array of paths to sound files.
        """
        return [str(s) for s in (SOUND_DIR / dir).iterdir()]
