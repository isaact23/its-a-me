import controller
from rule import Rule
from colors import *

BOX0 = 0, 12, 2, 13
BOX1 = 1, 13, 3, 14
BOX2 = 2, 15, 4, 16
BOX3 = 3, 16, 5, 17
BOX4 = 4, 18, 6, 19
BOX5 = 5, 19, 7, 20
BOX6 = 6, 21, 8, 22
BOX7 = 7, 22, 9, 23
BOX8 = 8, 24, 10, 25
BOX9 = 9, 25, 11, 26


class Game:
    """
    Control all game logic for Glass Stepping Stones. There are multiple 'modes' which
    govern how rules are generated for lights and how input is handled.
    Mode 100 - attract
    Mode 200 - startup
    Mode 300 - step
    Mode 400 - correct
    Mode 500 - fail
    Mode 600 - win
    """
    def __init__(self, controller, grid):
        """
        Initialize Game.
        :param controller: LED controller.
        :param grid: Segment container class.
        """
        self.controller = controller
        self.grid = grid
        self.mode = 100
        self.mode_initialized = False
        self.mode_start_time = 0

    def update(self):
        """
        Called every frame - update the game state, LEDs, etc. based on input and timing.
        """
        # Mode 100 - attract sequence 1
        if self.mode == 100:
            if not self.mode_initialized:
                self.grid.get_seg(27).set_rule(Rule().stripes((RED, ORANGE), width=8).animate(10).fade_in(2, 1))
                self.grid.get_seg(28).set_rule(Rule().stripes((RED, ORANGE), width=8).animate(10).fade_in(2, 1))

                # Have 5 boxes fade in and out in an orange color
                """
                box_rules = []
                for i in range(5):
                    box_rules.append(Rule().fill(ORANGE).fade_in(0.25, 4 + 0.75 * i).fade_out(0.25, 4.5 + 0.75 * i))
                boxes = [BOX0, BOX3, BOX4, BOX7, BOX8]
                for i, box in enumerate(boxes):
                    for seg in box:
                        self.grid.get_seg(seg).set_rule(box_rules[i])
                """
                """self.grid.get_seg(12).set_rule(Rule().stripes(RAINBOW, width=5).fade_in(2, 1).offset(3))
                self.grid.get_seg(15).set_rule(Rule().stripes(RAINBOW, width=5).fade_in(2, 1).offset(18))
                self.grid.get_seg(18).set_rule(Rule().stripes(RAINBOW, width=5).animate(10).fade_in(2, 1))
                self.grid.get_seg(21).set_rule(Rule().stripes(RAINBOW, width=5).animate(10).fade_in(2, 1))
                self.grid.get_seg(24).set_rule(Rule().stripes(RAINBOW, width=5).animate(10).fade_in(2, 1))"""

                right = controller.MultiSegment(self.grid, 12, 2, 16, 4, 18, 21, 24, 10, 11, 26,
                                                9, 22, 7, 20, 17, 14, 1, 0,
                                                flipped_segs=(4, 26, 9, 22, 20, 17, 14, 1, 0))
                right.set_rule(Rule().stripes(RAINBOW, width=27).animate(20))

                self.mode_initialized = True
