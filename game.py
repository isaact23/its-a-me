import time, keyboard
import sounds
from controller import MultiSegment
from rule import Rule
from colors import *

# TODO: Review iosoft.blog
# https://iosoft.blog/2020/09/29/raspberry-pi-multi-channel-ws2812/

CASCADE_TIME = 0.8

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

    def __init__(self, control, grid):
        """
        Initialize Game.
        :param controller: LED controller.
        :param grid: Segment container class.
        """
        self.controller = control
        self.grid = grid
        self.mode = 200
        self.mode_initialized = False
        self.start_time = 0
        self.sound_player = sounds.SoundPlayer()

        # Variables used by update_mode()
        self.undertale_count = 0

    def update(self):
        """
        Called every frame - update the game state, LEDs, etc. based on input and timing.
        """
        # Initialize color mode if not already initialized
        if not self.mode_initialized:
            self.init_mode()
            self.mode_initialized = True
            self.start_time = time.time()

        # Run loop to update mode - checks for button presses, user inputs, timer, etc.
        self.update_mode()

    def init_mode(self):
        """
        Initialize Rules for Segments for mode specified in self.mode.
        """
        # Mode 100 - attract sequence 1
        if self.mode == 100:
            # Railings are moving red/orange stripes
            self.grid.get_seg(27).set_rule(Rule().stripes((RED, ORANGE), width=8).animate(10).fade_in(2, 1))
            self.grid.get_seg(28).set_rule(Rule().stripes((RED, ORANGE), width=8).animate(10).fade_in(2, 1))

        elif self.mode == 101:
            # Have 5 boxes fade in and out in an orange color
            box_rules = []
            for i in range(5):
                box_rules.append(Rule().fill(ORANGE).fade_in(0.25, 4 + 0.75 * i).fade_out(0.25, 4.5 + 0.75 * i))
            boxes = [BOX0, BOX3, BOX4, BOX7, BOX8]
            for i, box in enumerate(boxes):
                for seg in box:
                    self.grid.get_seg(seg).set_rule(box_rules[i])

        elif self.mode == 102:
            # Have a white light zoom around the strip
            multi_seg = MultiSegment(self.grid, 12, 2, 16, 4, 18, 21, 24, 10, 11, 26,
                                                9, 22, 7, 20, 17, 14, 1, 0,
                                                flipped_segs=(4, 26, 9, 22, 20, 17, 14, 1, 0))
            multi_seg.set_rule(Rule().fill(WHITE, -15, 0).animate(100))
            # multi_seg.set_rule(Rule().stripes(RAINBOW, width=27).animate(20).fade_in(1, 2))

        elif self.mode == 200:
            row1 = MultiSegment(self.grid, 10, 11, 24, 25, 26, 8, 9).set_rule(Rule().fill(WHITE).fade_in(0, 0).fade_out(1, 2))
            row2 = MultiSegment(self.grid, 21, 6, 22, 7, 23).set_rule(Rule().fill(WHITE).fade_in(0, CASCADE_TIME).fade_out(1, 2 + CASCADE_TIME))
            row2 = MultiSegment(self.grid, 18, 4, 19, 5, 20).set_rule(Rule().fill(WHITE).fade_in(0, CASCADE_TIME * 2).fade_out(1, 2 + CASCADE_TIME * 2))
            row2 = MultiSegment(self.grid, 15, 2, 16, 3, 17).set_rule(Rule().fill(WHITE).fade_in(0, CASCADE_TIME * 3).fade_out(1, 2 + CASCADE_TIME * 3))
            row2 = MultiSegment(self.grid, 12, 0, 13, 1, 14).set_rule(Rule().fill(WHITE).fade_in(0, CASCADE_TIME * 4).fade_out(1, 2 + CASCADE_TIME * 4))

        elif self.mode == 300:
            left = MultiSegment(self.grid, 0, 12, 2).set_rule(Rule().fill(WHITE).blink(0.5, 1.5))
            right = MultiSegment(self.grid, 1, 14, 3).set_rule(Rule().fill(WHITE).blink(0.5, 1.5))
            mid = self.grid.get_seg(13).set_rule(Rule().fill(WHITE).blink(0.5, 0.5))


    def update_mode(self):
        """
        Run update loop constantly - check for button presses, user input, timer, etc.
        """
        time_elapsed = time.time() - self.start_time
        if self.mode <= 199:
            # On space press, move to stage 2 - start the game.
            if keyboard.is_pressed('space'):
                self.set_mode(200, clear_grid=True, clear_railings=True)
                self.undertale_count = 0
            elif self.mode == 100:
                self.set_mode(101)
            elif self.mode == 101:
                if time_elapsed > 10:
                    self.set_mode(102)
            elif self.mode == 102:
                if time_elapsed > 10:
                    self.set_mode(100)
        elif self.mode <= 299:
            if self.undertale_count < 5 and time_elapsed > self.undertale_count * CASCADE_TIME:
                self.sound_player.play(sounds.UNDERTALE)
                self.undertale_count += 1
            if time_elapsed > 7:
                self.set_mode(300)

    def set_mode(self, mode, clear_grid=False, clear_railings=False):
        """
        Prepare for a new mode.
        """
        self.mode = mode
        self.start_time = time.time()
        self.mode_initialized = False
        self.grid.clear_rules(clear_grid, clear_railings)
