from mode import Mode
from mode200 import Mode200
from settings import *


# Mode 100 - Superclass for attract modes
class Mode100(Mode):
    def __init__(self, controller, grid, screen):
        super().__init__(controller, grid, screen)

    def update(self, pressed_keys):
        if pressed_keys[KEY_START]:
            print("Starting!")
            return Mode200(self.controller, self.grid, self.screen)

        super().update(pressed_keys)
