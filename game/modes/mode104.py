from mode100 import Mode100
from settings import *
from rule import Rule
from controller import MultiSegment


# Mode 104 - Attract sequence mode 4
class Mode104(Mode100):
    def __init__(self, controller, grid, screen):
        super().__init__(controller, grid, screen)

        # Set up cool rainbow effect
        multi_segs = []
        multi_segs.append(MultiSegment(self.grid, 22, 26, 30, 34, 38, 20, 21))

        multi_segs.append(MultiSegment(self.grid, 18, 39))
        multi_segs.append(MultiSegment(self.grid, 16, 40))

        multi_segs.append(MultiSegment(self.grid, 14, 35, 19, 41))
        multi_segs.append(MultiSegment(self.grid, 12, 36, 17))

        multi_segs.append(MultiSegment(self.grid, 10, 31, 15, 37))
        multi_segs.append(MultiSegment(self.grid, 8, 32, 13))

        multi_segs.append(MultiSegment(self.grid, 6, 27, 11, 33))
        multi_segs.append(MultiSegment(self.grid, 4, 28, 9))

        multi_segs.append(MultiSegment(self.grid, 2, 23, 7, 29))

        multi_segs.append(MultiSegment(self.grid, 24, 5))
        multi_segs.append(MultiSegment(self.grid, 3, 25))

        for i, multi_seg in enumerate(multi_segs):
            rule = Rule().hue_linear(5).fade_in(1, 0).fade_out(1, 5).animate(40)
            if 1 <= i <= 2:
                rule.offset(SEG_WIDTH * 4)
            elif 3 <= i <= 4:
                rule.offset(SEG_WIDTH * 3)
            elif 5 <= i <= 6:
                rule.offset(SEG_WIDTH * 2)
            elif 7 <= i <= 8:
                rule.offset(SEG_WIDTH)
            elif 10 <= i <= 11:
                rule.offset(SEG_WIDTH)

            multi_seg.set_rule(rule)

    def update(self, pressed_keys):
        if self.time_elapsed > 7:
            return 105

        return super().update(pressed_keys)
