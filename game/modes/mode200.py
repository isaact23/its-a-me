from mode import Mode
from settings import *


# Mode 200 - Superclass for tutorial modes
class Mode200(Mode):
    def __init__(self, controller, grid, screen):
        super().__init__(controller, grid, screen)

    def update(self, pressed_keys):
        return super().update(pressed_keys)
