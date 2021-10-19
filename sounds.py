from pygame import mixer

mixer.init()
mixer.music.set_volume(1)

UNDERTALE = mixer.Sound("sounds/undertale.wav")

SHATTER_1 = mixer.Sound("sounds/Glass Shatter 1.wav")
SHATTER_2 = mixer.Sound("sounds/Glass Shatter 2.wav")
SHATTER_3 = mixer.Sound("sounds/Glass Shatter 3.wav")

FINAL_FANTASY = mixer.Sound("sounds/Final Fantasy VII - One Winged Angel.ogg")


class SoundPlayer:
    def __init__(self):
        pass

    def play(self, sound):
        """
        :param sound: The Sound object to play.
        """
        sound.play()

    def stop(self):
        mixer.stop()
