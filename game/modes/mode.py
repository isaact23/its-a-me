# A Mode defines a state the game can be in.
from settings import *
from sounds import SoundPlayer
import time

# Mode is the superclass for all game modes.
class Mode:
    def __init__(self, controller, grid, screen):
        self.controller = controller
        self.grid = grid
        self.screen = screen
        self.sound_player = SoundPlayer()

        # Reset start time on EVERY mode change.
        self.start_time = time.time()
        self.time_elapsed = 0

    # Update this Mode every frame. Return the mode to transition to.
    def update(self, pressed_keys):
        self.time_elapsed = time.time() - self.start_time
        self.sound_player.update()

        # Relay
        if pressed_keys[KEY_MUSHROOM_UP]:
            self.controller.mushroom_up()
        elif pressed_keys[KEY_MUSHROOM_DOWN]:
            self.controller.mushroom_down()

        return self
