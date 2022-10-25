from all_modes import *
from colors import *
from settings import *
from rule import Rule

# Mode 102 - Attract sequence mode 2
class Mode102(Mode100):
    def __init__(self, controller, grid, screen):
        super().__init__(controller, grid, screen)

        # Have 5 boxes fade in and out in an orange color
        box_ids = 0, 3, 4, 7, 8  # [BOX0, BOX3, BOX4, BOX7, BOX8]
        for i, box_id in enumerate(box_ids):
            box_rule = Rule().fill(ORANGE).fade_in(0.25, 0.75 * i).fade_out(0.25, 0.5 + 0.75 * i)
            for seg_id in BOXES[box_id]:
                self.grid.get_seg(seg_id).set_rule(box_rule)

    def update(self, pressed_keys):
        if self.time_elapsed > 4:
            return Mode103(self.controller, self.grid, self.screen)

        return super().update(pressed_keys)
