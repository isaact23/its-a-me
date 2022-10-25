from all_modes import *


# Mode 101 - Attract sequence mode 1
class Mode101(Mode100):
    def __init__(self, controller, grid, screen):
        super().__init__(controller, grid, screen)

    def update(self, pressed_keys):
        if self.time_elapsed > 4:
            return Mode102(self.controller, self.grid, self.screen)

        return super().update(pressed_keys)
