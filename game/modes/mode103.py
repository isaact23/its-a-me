from all_modes import *
from colors import *
from rule import Rule
from controller import MultiSegment

# Mode 103 - Attract sequence mode 3
class Mode103(Mode100):
    def __init__(self, controller, grid, screen):
        super().__init__(controller, grid, screen)

        # Have a white light zoom around the strip
        multi_seg = MultiSegment(self.grid, 22, 4, 27, 8, 30, 34, 38, 20, 21, 41,
                                 17, 36, 13, 33, 29, 25, 3, 2,
                                 flipped_segs=(8, 41, 17, 36, 33, 29, 25, 3, 2))
        multi_seg.set_rule(Rule().fill(WHITE, -15, 0).animate(60))

    def update(self, pressed_keys):
        if self.time_elapsed > 5:
            return Mode104(self.controller, self.grid, self.screen)

        return super().update(pressed_keys)
