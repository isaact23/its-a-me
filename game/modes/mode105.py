from mode100 import Mode100
from colors import *
from rule import Rule
from controller import MultiSegment


# Mode 105 - Attract sequence mode 5
class Mode105(Mode100):
    def __init__(self, controller, grid, screen):
        super().__init__(controller, grid, screen)

        # Set up fall colors revolving around board perimeter
        MultiSegment(self.grid, 22, 26, 30, 34, 38, 20, 21, 41, 37, 33, 29, 25, 3, 2,
                     flipped_segs=(41, 37, 33, 29, 25, 3, 2)).set_rule(
            Rule().stripes((RED, ORANGE, YELLOW), 12).animate(30).fade_in(1, 0).fade_out(1, 5)
        )

    def update(self, pressed_keys):
        if self.time_elapsed > 7:
            return 101

        return super().update(pressed_keys)
