import enum, pathlib, random
from pygame import mixer

SOUND_DIR = pathlib.Path(__file__).parent / 'media/sounds'


class SoundPlayer:
    def __init__(self):
        self.mode = self.Mode.NONE
        self.attract_music = self._get_sounds_from('music/attract_music')
        self.tutorial_music = self._get_sounds_from('music/tutorial_music')
        self.play_music = self._get_sounds_from('music/play_music')
        self.win_music = self._get_sounds_from('music/win_music')
        self.lose_music = self._get_sounds_from('music/lose_music')

        # Initialize pygame sound mixer
        mixer.init(44100, -16, 1, 1024)
        mixer.music.set_volume(1)

        self.sound_effects = self.SoundEffects()

    # All possible states for the sound player to be in.
    class Mode(enum.Enum):
        NONE = 0
        ATTRACT = 1
        TUTORIAL = 2
        PLAY = 3
        WIN = 4
        LOSE = 5

    # Sound effects
    class SoundEffects():
        BOWSER_LAUGH = "bowser_laugh.ogg"

        def __init__(self):
            self.sound_files = {}

        # Get the corresponding sound object from a sound name.
        def get_sound_obj(self, sound_name):
            sound_file = self.sound_files.get(sound_name)
            if sound_file is None:
                try:
                    sound_file = mixer.Sound(SOUND_DIR / ('sfx/' + sound_name))
                    self.sound_files[sound_name] = sound_file
                    return sound_file
                except Exception:
                    print("Error loading sound file", str(sound_name))
                    return None
            return sound_file

    # Update loop. Restart songs if necessary
    def update(self):
        if not mixer.music.get_busy():
            if self.mode == self.Mode.ATTRACT:
                self._play_music(random.choice(self.attract_music))
            elif self.mode == self.Mode.TUTORIAL:
                self._play_music(random.choice(self.tutorial_music))
            elif self.mode == self.Mode.PLAY:
                self._play_music(random.choice(self.play_music))

    # Update mode.
    def set_mode(self, mode):
        if mode != self.mode:
            self.stop()
            self.mode = mode
            if mode == self.Mode.WIN:
                self._play_music(random.choice(self.win_music))
            elif mode == self.mode.LOSE:
                self._play_music(random.choice(self.lose_music))

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
            print("Error playing music", str(music))

    # Play a sound file.
    def play_sound(self, sound):
        sound_obj = self.sound_effects.get_sound_obj(sound)
        if sound_obj is None:
            print("Error playing sound", str(sound))
        else:
            sound_obj.play()

    # Import sounds from directories
    def _get_sounds_from(self, dir):
        """
        Return all sounds from a given subdirectory of sounds.
        :param dir: The directory to retrive sounds from.
        :return: An array of paths to sound files.
        """
        return [str(s) for s in (SOUND_DIR / dir).iterdir()]
