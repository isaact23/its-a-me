import math, pathlib, random, time

import pygame

import colors
from sounds import SoundPlayer
from colors import *
from controller import MultiSegment
from rule import Rule, Mode

# Keys
KEY_START = pygame.K_f
BOX_KEYS = [pygame.K_v, pygame.K_y,
             pygame.K_d, pygame.K_j,
             pygame.K_a, pygame.K_z,
             pygame.K_m, pygame.K_w,
             pygame.K_x, pygame.K_t]
RELAY_KEY = pygame.K_r

# Tutorial box numbers
TUTORIAL_BOXES = (5, 0, 8)

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
WHACK_TIME = 10  # How many seconds before a tile despawns

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
        self.sound_player = SoundPlayer()
        self.mode = 100
        self.mode_initialized = False
        self.mode_initializing = True
        self.start_time = time.time()

        # Variables changed during gameplay
        self.square_count = 0
        self.active_squares = {i: -1 for i in range(10)}
        self.score = 0
        self.max_score = 0
        self.relay_key_pressed = False

        # Initialize images for Pygame
        sound_dir = pathlib.Path(__file__).parent / 'media/images'
        self.image_cloud = pygame.image.load(str(sound_dir / 'lakitu.png')).convert()
        self.image_cloud = pygame.transform.scale(self.image_cloud, (800, 800))
        self.image_toad = pygame.image.load(str(sound_dir / 'toad.png')).convert()
        self.image_toad = pygame.transform.scale(self.image_toad, (360, 400))
        self.image_mole = pygame.image.load(str(sound_dir / 'mole.png')).convert()
        self.image_mole = pygame.transform.scale(self.image_mole, (1000, 800))

        # Initialize text for Pygame
        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", 50)
        self.toad_text1 = self.font.render("Hi! I need your help to collect the power", 1, BLACK)
        self.toad_text2 = self.font.render("stars! Step on the square to start!", 1, BLACK)
        self.toad_text3 = self.font.render("Great! Keep it up!", 1, BLACK)
        self.toad_text4 = self.font.render("One square to go!", 1, BLACK)
        self.toad_text5 = self.font.render("Great! Now get ready for the real game!", 1, BLACK)

        # Initialize miscellaneous Pygame objects
        self.mole_text_cover = pygame.Rect(50, 50, 1000, 50)

    def update(self, pressed_keys):
        """
        Called every frame - update the game state, LEDs, etc. based on input and timing.
        """
        time_elapsed = time.time() - self.start_time
        self.sound_player.update()

        # Relay code
        if pressed_keys[RELAY_KEY]:
            if not self.relay_key_pressed:
                self.relay_key_pressed = True
                self.controller.flip_relay()
        else:
            self.relay_key_pressed = False

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

            # On space press, move to stage 2 - start the game.
            if pressed_keys[KEY_START]:
                print("Starting!")
                self.set_mode(200, clear=True)
                self.sound_player.stop()

            elif self.mode == 100:
                if not self.mode_initialized:
                    # Render cloud GUI
                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_cloud, (550, 100))
                    pygame.display.update()

                    # Play attract music
                    self.sound_player.set_mode(SoundPlayer.Mode.ATTRACT)

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

        # Mode 200-299 - tutorial mode
        elif self.mode <= 299:
            if self.mode == 200:
                box_no = TUTORIAL_BOXES[0]

                if not self.mode_initialized:
                    # Render toad GUI
                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_toad, (100, 50))
                    self.screen.blit(self.toad_text1, (500, 50))
                    self.screen.blit(self.toad_text2, (500, 100))
                    pygame.display.update()

                    # Play tutorial music
                    self.sound_player.set_mode(SoundPlayer.Mode.TUTORIAL)

                    # Start light strip pattern
                    box = BOXES[box_no]
                    multiseg = MultiSegment(self.grid, box[0], box[1], box[2], box[3], flipped_segs=(box[0], box[3]))
                    multiseg.set_rule(Rule().stripes((WHITE, OFF), 6).animate(16))

                if pressed_keys[BOX_KEYS[box_no]]:
                    self.set_mode(201, clear=True)

            elif self.mode == 201:
                box_no = TUTORIAL_BOXES[1]

                if not self.mode_initialized:
                    # Render toad GUI
                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_toad, (100, 50))
                    self.screen.blit(self.toad_text3, (500, 50))
                    pygame.display.update()

                    # Start light strip pattern
                    box = BOXES[box_no]
                    multiseg = MultiSegment(self.grid, box[0], box[1], box[2], box[3], flipped_segs=(box[0], box[3]))
                    multiseg.set_rule(Rule().stripes((WHITE, OFF), 6).animate(16))

                if pressed_keys[BOX_KEYS[box_no]]:
                    self.set_mode(202, clear=True)

            elif self.mode == 202:
                box_no = TUTORIAL_BOXES[2]

                if not self.mode_initialized:
                    # Render toad GUI
                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_toad, (100, 50))
                    self.screen.blit(self.toad_text4, (500, 50))
                    pygame.display.update()

                    # Start light strip pattern
                    box = BOXES[box_no]
                    multiseg = MultiSegment(self.grid, box[0], box[1], box[2], box[3], flipped_segs=(box[0], box[3]))
                    multiseg.set_rule(Rule().stripes((WHITE, OFF), 6).animate(16))

                if pressed_keys[BOX_KEYS[box_no]]:
                    self.set_mode(203, clear=True)

            # Tutorial complete; prepare for real game
            elif self.mode == 203:
                if not self.mode_initialized:
                    # Render toad GUI
                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_toad, (100, 50))
                    self.screen.blit(self.toad_text5, (500, 50))
                    pygame.display.update()

                    # Play powerup stinger
                    self.sound_player.set_mode(SoundPlayer.Mode.STINGER, SoundPlayer.Stingers.SMG_POWERUP)

                if time_elapsed > 10:
                    self.set_mode(300)

        # Modes 300-399 - gameplay
        elif self.mode <= 399:
            # Wait for user input on first row
            if self.mode == 300:
                if not self.mode_initialized:
                    # Play game music
                    self.sound_player.set_mode(SoundPlayer.Mode.PLAY)

                    # Render GUI
                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_mole, (550, 150))
                    pygame.display.update()

                    # Initialize rules for side rails
                    self.grid.get_seg(0).set_rule(Rule().stripes((RED, OFF, OFF, OFF, OFF, BLUE, OFF, OFF, OFF, OFF), 3).animate(30))
                    self.grid.get_seg(1).set_rule(Rule().stripes((RED, OFF, OFF, OFF, OFF, BLUE, OFF, OFF, OFF, OFF), 3).animate(30))

                # Display score
                score_text = self.font.render("Stars collected: " + str(self.score) + " / " + str(self.max_score), 1, BLACK)
                pygame.draw.rect(self.screen, WHITE, self.mole_text_cover)
                self.screen.blit(score_text, (200, 50))
                pygame.display.update()

                # Spawn more squares after some time
                if time_elapsed < 25:
                    exp = 2 * math.exp(time_elapsed / 12) - 1
                    if exp > self.square_count:
                        self.max_score += 1
                        self.square_count = math.ceil(exp)
                        available_squares = [i for i in range(10) if self.active_squares[i] < 0]
                        if len(available_squares) > 0:
                            chosen_square = random.choice(available_squares)
                            self.active_squares[chosen_square] = time.time()
                            multi_segment = MultiSegment(self.grid, *BOXES[chosen_square], flipped_segs=[BOXES[chosen_square][0], BOXES[chosen_square][3]])
                            multi_segment.set_rule(
                                Rule().stripes((random.choice(
                                    [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE]
                                ), OFF), 6).animate(20)
                            )


                for i in range(10):
                    # Check to see if active squares have been stepped on
                    if pressed_keys[BOX_KEYS[i]]:
                        if self.active_squares[i] > 0:
                            self.active_squares[i] = -1
                            self.score += 1
                            for j in BOXES[i]:
                                self.grid.get_seg(j).set_rule(None)

                    # Check to see if active squares have run out of time
                    curr_time = time.time()
                    if curr_time - self.active_squares[i] > WHACK_TIME:
                        self.active_squares[i] = -1
                        for j in BOXES[i]:
                            self.grid.get_seg(j).set_rule(None)

                if time_elapsed > 30:
                    self.set_mode(400, clear=True)

        # Modes 400-499: Final win sequence
        elif self.mode <= 499:
            if self.mode == 400:
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

        # Reset variables changed during gameplay
        self.square_count = 0
        self.active_squares = {i: -1 for i in range(10)}
        self.score = 0
        self.max_score = 0
        self.relay_key_pressed = False
