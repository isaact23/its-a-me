import pathlib, random, time

import pygame

import colors
import sounds
from colors import *
from controller import MultiSegment
from rule import Rule, Mode

# Keys
KEY_START = pygame.K_f

# Segment numbers
BOXES = ((2, 22, 4, 23),
         (3, 24, 5, 25),
         (6, 26, 8, 27),
         (7, 28, 9, 29),
         (10, 30, 12, 31),
         (11, 32, 13, 33),
         (14, 34, 16, 35),
         (15, 36, 17, 37),
         (18, 38, 20, 39),
         (19, 40, 21, 41))
RAILS = (0, 1)
GRID = tuple(i for i in range(2, 42))
ALL_SEGS = tuple(i for i in range(42))

SEG_WIDTH = 12

class Game:
    """
    Control all game logic. There are multiple 'modes' which
    govern how rules are generated for lights and how input is handled.
    Mode 100 - attract
    Mode 200 - rules
    Mode 300 - gameplay
    Mode 400 - scores
    """

    def __init__(self, control, grid, screen):
        """
        Initialize Game.
        :param control: LED controller.
        :param grid: Segment container class.
        """
        self.controller = control
        self.grid = grid
        self.screen = screen
        self.sound_player = sounds.SoundPlayer()
        self.mode = 100
        self.mode_initialized = False
        self.mode_initializing = True
        self.start_time = time.time()

        # Initialize images for Pygame
        sound_dir = pathlib.Path(__file__).parent / 'media/images'
        self.image_cloud = pygame.image.load(sound_dir / 'lakitu.png').convert()
        self.image_cloud = pygame.transform.scale(self.image_cloud, (800, 800))

        self.screen.fill(WHITE)
        self.screen.blit(self.image_cloud, (550, 100))
        pygame.display.flip()

    def update(self, pressed_keys):
        """
        Called every frame - update the game state, LEDs, etc. based on input and timing.
        """
        time_elapsed = time.time() - self.start_time

        # Mode 0-99 - testing purposes only
        if self.mode <= 99:
            # MultiSegment(self.grid, 12, 15, 18, 21, 24, 10, 11).set_rule(Rule().hue(60, 310, 0.1))
            # MultiSegment(self.grid, 12, 15, 18, 21, 24, 10, 11).set_rule(Rule().fill(RED).crop(40, 990))
            # MultiSegment(self.grid, *ALL_SEGS).set_rule(
            #    Rule().fill(WHITE)
            # )
            # MultiSegment(self.grid, *ALL_SEGS).set_rule(Rule().fill(WHITE))
            if not self.mode_initialized:
                self.grid.get_seg(0).set_rule(
                    Rule().stripes((RED, YELLOW), 5).animate(10)
                )

        # Mode 100-199 - attract sequence
        elif self.mode <= 199:
            self.sound_player.update()

            # On space press, move to stage 2 - start the game.
            if pressed_keys[KEY_START]:
                print("Starting!")
                self.set_mode(200, clear=True)
                self.sound_player.stop()

            elif self.mode == 100:
                if not self.mode_initialized:
                    # Play attract music
                    self.sound_player.set_mode(sounds.SoundPlayer.Mode.ATTRACT)

                    # Railings are red/orange moving stripes in intro
                    self.grid.get_seg(0).set_rule(Rule().stripes((RED, WHITE, BLUE), width=8).animate(10).fade_in(2, 1))
                    self.grid.get_seg(1).set_rule(Rule().stripes((RED, WHITE, BLUE), width=8).animate(10).fade_in(2, 1))

                    # multi_seg = MultiSegment(self.grid, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                    #                         17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                    #                         34, 35, 36, 37, 38, 39, 40, 41,
                    #                         flipped_segs=())
                    # multi_seg = MultiSegment(self.grid, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                    #                         flipped_segs=())
                    # multi_seg.set_rule(Rule().fill(WHITE, 0, 1).animate(8))

                if time_elapsed > 4:
                    self.set_mode(101)

            elif self.mode == 101:
                if not self.mode_initialized:
                    # Have 5 boxes fade in and out in an orange color
                    box_ids = 0, 3, 4, 7, 8  # [BOX0, BOX3, BOX4, BOX7, BOX8]
                    for i, box_id in enumerate(box_ids):
                        box_rule = Rule().fill(ORANGE).fade_in(0.25, 0.75 * i).fade_out(0.25, 0.5 + 0.75 * i)
                        for seg_id in BOXES[box_id]:
                            self.grid.get_seg(seg_id).set_rule(box_rule)
                if time_elapsed > 5:
                    self.set_mode(102)

            elif self.mode == 102:
                if not self.mode_initialized:
                    # Have a white light zoom around the strip
                    multi_seg = MultiSegment(self.grid, 22, 4, 27, 8, 30, 34, 38, 20, 21, 41,
                                             17, 36, 13, 33, 29, 25, 3, 2,
                                             flipped_segs=(8, 41, 17, 36, 33, 29, 25, 3, 2))
                    multi_seg.set_rule(Rule().fill(WHITE, -15, 0).animate(60))
                if time_elapsed > 5:
                    self.set_mode(103)

            elif self.mode == 103:
                if not self.mode_initialized:
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
                if time_elapsed > 7:
                    self.set_mode(104)

            elif self.mode == 104:
                if not self.mode_initialized:
                    MultiSegment(self.grid, 22, 26, 30, 34, 38, 20, 21, 41, 37, 33, 29, 25, 3, 2,
                                 flipped_segs=(41, 37, 33, 29, 25, 3, 2)).set_rule(
                        Rule().stripes((RED, ORANGE, YELLOW), 12).animate(30).fade_in(1, 0).fade_out(1, 5)
                    )
                if time_elapsed > 7:
                    self.set_mode(101)

            elif self.mode == 105:
                if not self.mode_initialized:
                    width = 6
                    speed = 50
                    MultiSegment(self.grid, 31, 35, 39, 20, 38, 16, 12, 30, 8, flipped_segs=(20, 38, 12, 30)).set_rule(
                        Rule().stripes((WHITE, BLACK), width).crop(-200, 0).animate(speed)
                    )
                    MultiSegment(self.grid, 32, 36, 40, 21, 41, 17, 13, 33, 9, flipped_segs=(41, 17, 33, 9)).set_rule(
                        Rule().stripes((WHITE, BLACK), width).crop(-200, 0).animate(speed)
                    )
                    MultiSegment(self.grid, 27, 23, 2, 22, 4, flipped_segs=(27, 23, 2)).set_rule(
                        Rule().stripes((WHITE, BLACK), width).crop(-200, 0).animate(speed)
                    )
                    MultiSegment(self.grid, 28, 24, 3, 25, 5, flipped_segs=(28, 24, 5)).set_rule(
                        Rule().stripes((WHITE, BLACK), width).crop(-200, 0).animate(speed)
                    )
                if time_elapsed > 9:
                    self.set_mode(101)

        # Mode 200-299 - transition to game
        elif self.mode <= 299:
            if self.mode == 200:
                if not self.mode_initialized:
                    pass

                if time_elapsed > 7:
                    self.set_mode(300)

        # Modes 300-399 - gameplay
        elif self.mode <= 399:
            # Wait for user input on first row
            if self.mode == 300:
                if not self.mode_initialized:
                    pass

        # Modes 400-499: Final win sequence
        elif self.mode <= 499:
            if not self.mode_initialized:
                pass

            if time_elapsed > 9:
                self.reset_game()

        # If we just initialized, prevent re-initialization on next update cycles.
        if self.mode_initializing:
            self.mode_initializing = False
        elif not self.mode_initialized:
            self.mode_initialized = True

    def set_mode(self, mode, clear=False):
        """
        Prepare for a new mode.
        """
        self.mode = mode
        self.start_time = time.time()
        self.mode_initialized = False
        self.mode_initializing = True
        if clear:
            self.grid.clear_rules()

        print("Set mode to", mode)

    def reset_game(self):
        """
        Re-initialize the game for a new round.
        """
        self.set_mode(100)
