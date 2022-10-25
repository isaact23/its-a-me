# A Mode defines a state the game can be in.
from settings import *
from sounds import SoundPlayer
from typing import TypeVar



# Mode is the superclass for all game modes.
class Mode:
    def __init__(self, controller, grid, screen):
        self.controller = controller
        self.grid = grid
        self.screen = screen
        self.sound_player = SoundPlayer()

    # Update this Mode every frame. Return the mode to transition to.
    def update(self, pressed_keys):

        # Relay
        if pressed_keys[KEY_MUSHROOM_UP]:
            self.controller.mushroom_up()
        elif pressed_keys[KEY_MUSHROOM_DOWN]:
            self.controller.mushroom_down()

        return self
