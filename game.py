# TODO: Use polymorphism: Create interface 'Mode' and have game.py call its methods.
# Implement Mode as all of the different modes in separate Python files, i.e. 401, 402, etc.

import math, pathlib, time

import pygame

from sounds import SoundPlayer
from colors import *
from controller import MultiSegment
from rule import Rule
from settings import *


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
        self.controller.mushroom_down()
        self.controller.flag_up()

        # Variables changed during gameplay
        self.animation_no = 0
        self.animation_start_time = time.time()
        self.square_count = 0
        self.active_squares = {i: -1 for i in range(10)}
        self.score = 0
        self.max_score = 0
        self.lives = 1
        self.star_start_time = 0
        self.bowser_start_time = 0

        # Initialize images for Pygame
        image_dir = pathlib.Path(__file__).parent / 'media/images'
        self.image_toad = pygame.image.load(str(image_dir / 'toad.png')).convert()
        self.image_toad = pygame.transform.scale(self.image_toad, (200, 240))
        self.image_toad2 = pygame.image.load(str(image_dir / 'toad2.jpeg')).convert()
        self.image_toad2 = pygame.transform.scale(self.image_toad2, (250, 360))
        self.image_game_over = pygame.image.load(str(image_dir / 'game_over.jpeg')).convert()
        self.image_game_over = pygame.transform.scale(self.image_game_over, (620, 400))
        self.image_oneup = pygame.image.load(str(image_dir / 'oneup.png')).convert()
        self.image_oneup = pygame.transform.scale(self.image_oneup, (300, 300))
        self.image_overlay = pygame.image.load(str(image_dir / 'overlay.png'))
        self.image_overlay = pygame.transform.scale(self.image_overlay, WINDOW_SIZE)
        self.image_star_array = {}
        for i in range(STAR_FRAMES):
            star_img = pygame.image.load(str(image_dir / ('star/frame_%02d_delay-0.06s.gif' % i))).convert()
            self.image_star_array[i] = pygame.transform.scale(star_img, (RECT_SIZE, RECT_SIZE))
        self.image_bowser_array = {}
        for i in range(BOWSER_FRAMES):
            bowser_img = pygame.image.load(str(image_dir / ('bowser/%03d.png' % i))).convert()
            bowser_img = pygame.transform.scale(bowser_img, WINDOW_SIZE)
            self.image_bowser_array[i] = bowser_img
        self.image_cloud_array = {}
        for i in range(CLOUD_FRAMES):
            cloud_img = pygame.image.load(str(image_dir / ('cloud/frame_%02d_delay-0.2s.gif' % i))).convert()
            self.image_cloud_array[i] = pygame.transform.scale(cloud_img, WINDOW_SIZE)
        self.image_goomba_array = {}
        for i in range(GOOMBA_FRAMES):
            goomba_img = pygame.image.load(str(image_dir / ('goomba/frame_%01d_delay-0.2s.gif' % i))).convert()
            self.image_goomba_array[i] = pygame.transform.scale(goomba_img, WINDOW_SIZE)
        self.image_mario_array = {}
        for i in range(MARIO_FRAMES):
            mario_img = pygame.image.load(str(image_dir / ('mario/frame_%02d_delay-0.13s.gif' % i))).convert()
            self.image_mario_array[i] = pygame.transform.scale(mario_img, (round(WINDOW_SIZE[0] * 0.7), round(WINDOW_SIZE[1] * 0.7)))

        # Initialize text for Pygame
        pygame.font.init()
        self.font = pygame.font.SysFont("dejavusans", 32)

        # Initialize miscellaneous Pygame objects
        self.rects = [
            (RECT_START_X, RECT_START_Y, RECT_SIZE, RECT_SIZE),
            (RECT_START_X, RECT_START_Y + RECT_SIZE + RECT_SPACING, RECT_SIZE, RECT_SIZE),
            (RECT_START_X + RECT_SIZE + RECT_SPACING, RECT_START_Y, RECT_SIZE, RECT_SIZE),
            (RECT_START_X + RECT_SIZE + RECT_SPACING, RECT_START_Y + RECT_SIZE + RECT_SPACING, RECT_SIZE, RECT_SIZE),
            (RECT_START_X + (RECT_SIZE + RECT_SPACING) * 2, RECT_START_Y, RECT_SIZE, RECT_SIZE),
            (RECT_START_X + (RECT_SIZE + RECT_SPACING) * 2, RECT_START_Y + RECT_SIZE + RECT_SPACING, RECT_SIZE,
             RECT_SIZE),
            (RECT_START_X + (RECT_SIZE + RECT_SPACING) * 3, RECT_START_Y, RECT_SIZE, RECT_SIZE),
            (RECT_START_X + (RECT_SIZE + RECT_SPACING) * 3, RECT_START_Y + RECT_SIZE + RECT_SPACING, RECT_SIZE,
             RECT_SIZE),
            (RECT_START_X + (RECT_SIZE + RECT_SPACING) * 4, RECT_START_Y, RECT_SIZE, RECT_SIZE),
            (RECT_START_X + (RECT_SIZE + RECT_SPACING) * 4, RECT_START_Y + RECT_SIZE + RECT_SPACING, RECT_SIZE,
             RECT_SIZE),
        ]
        self.pygame_rects = [pygame.Rect(*x) for x in self.rects]

    def update(self, pressed_keys):
        """
        Called every frame - update the game state, LEDs, etc. based on input and timing.
        """
        time_elapsed = time.time() - self.start_time

        self.sound_player.update()

        # Relay
        if pressed_keys[KEY_MUSHROOM_UP]:
            self.controller.mushroom_up()
        elif pressed_keys[KEY_MUSHROOM_DOWN]:
            self.controller.mushroom_down()

        # Mode 100-199 - attract sequence
        if self.mode <= 199:

            # If any tile is pressed, start tutorial mode.
            for key in BOX_KEYS:
                if pressed_keys[key]:
                    print("Starting!")
                    self.set_mode(200, clear=True)
                    self.sound_player.stop()
                    self.controller.mushroom_down()
                    break

            # Choose frame
            animation_time_elapsed = time.time() - self.animation_start_time
            if self.animation_no == 0:  # Cloud animation
                frame = math.floor(animation_time_elapsed * CLOUD_FRAMERATE) % CLOUD_FRAMES
                self.screen.fill(BLACK)
                self.screen.blit(self.image_cloud_array[frame], (-20, -20))
                if animation_time_elapsed > CLOUD_ANIMATION_SECS:
                    self.animation_no = 1
                    self.animation_start_time = time.time()
            elif self.animation_no == 1:  # Goomba animation
                frame = math.floor(animation_time_elapsed * GOOMBA_FRAMERATE) % GOOMBA_FRAMES
                self.screen.fill(BLACK)
                self.screen.blit(self.image_goomba_array[frame], (-20, -20))
                if animation_time_elapsed > GOOMBA_ANIMATION_SECS:
                    self.animation_no = 2
                    self.animation_start_time = time.time()
            elif self.animation_no == 2:  # Mario animation
                frame = math.floor(animation_time_elapsed * MARIO_FRAMERATE) % MARIO_FRAMES
                self.screen.fill(WHITE)
                self.screen.blit(self.image_mario_array[frame], (100, 140))
                if animation_time_elapsed > MARIO_ANIMATION_SECS:
                    self.animation_no = 0
                    self.animation_start_time = time.time()

            # Setup attract mode
            if self.mode == 100:
                # Railings are red/orange moving stripes in intro
                self.grid.get_seg(0).set_rule(Rule().stripes((RED, WHITE, BLUE), width=8).animate(10).fade_in(2, 1))
                self.grid.get_seg(1).set_rule(Rule().stripes((RED, WHITE, BLUE), width=8).animate(10).fade_in(2, 1))

                # Pumpkins
                self.grid.get_seg(42).set_rule(Rule().stripes((WHITE, OFF), width=1).animate(2).fade_in(2, 1))  # Toad
                self.grid.get_seg(43).set_rule(Rule().hue_wave(0, 50, 1, Rule.Mode.PIXEL).animate(4))  # Mario
                self.grid.get_seg(44).set_rule(Rule().hue_wave(70, 170, 1, Rule.Mode.PIXEL).animate(4))  # Luigi

                # Initialize animation
                self.animation_no = 2
                self.animation_start_time = time.time()

                # Play attract music
                self.sound_player.set_mode(SoundPlayer.Mode.ATTRACT)

                self.set_mode(101)

            elif self.mode == 101:
                if time_elapsed > 4:
                    self.set_mode(102)

            elif self.mode == 102:
                if not self.mode_initialized:
                    # Have 5 boxes fade in and out in an orange color
                    box_ids = 0, 3, 4, 7, 8  # [BOX0, BOX3, BOX4, BOX7, BOX8]
                    for i, box_id in enumerate(box_ids):
                        box_rule = Rule().fill(ORANGE).fade_in(0.25, 0.75 * i).fade_out(0.25, 0.5 + 0.75 * i)
                        for seg_id in BOXES[box_id]:
                            self.grid.get_seg(seg_id).set_rule(box_rule)
                if time_elapsed > 5:
                    self.set_mode(103)

            elif self.mode == 103:
                if not self.mode_initialized:
                    # Have a white light zoom around the strip
                    multi_seg = MultiSegment(self.grid, 22, 4, 27, 8, 30, 34, 38, 20, 21, 41,
                                             17, 36, 13, 33, 29, 25, 3, 2,
                                             flipped_segs=(8, 41, 17, 36, 33, 29, 25, 3, 2))
                    multi_seg.set_rule(Rule().fill(WHITE, -15, 0).animate(60))
                if time_elapsed > 5:
                    self.set_mode(104)

            elif self.mode == 104:
                if not self.mode_initialized:
                    self.controller.mushroom_up()
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
                    self.controller.mushroom_down()
                    self.set_mode(105)

            elif self.mode == 105:
                if not self.mode_initialized:
                    MultiSegment(self.grid, 22, 26, 30, 34, 38, 20, 21, 41, 37, 33, 29, 25, 3, 2,
                                 flipped_segs=(41, 37, 33, 29, 25, 3, 2)).set_rule(
                        Rule().stripes((RED, ORANGE, YELLOW), 12).animate(30).fade_in(1, 0).fade_out(1, 5)
                    )
                if time_elapsed > 7:
                    self.set_mode(102)

        # Mode 200-299 - tutorial mode
        elif self.mode <= 299:
            if self.mode == 200:
                box_no = TUTORIAL_BOXES[0]

                if not self.mode_initialized:
                    # Render toad GUI
                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_toad, (60, 200))

                    # Play tutorial music
                    self.sound_player.set_mode(SoundPlayer.Mode.TUTORIAL)

                    # Play toad sound
                    self.sound_player.play_sound(SoundPlayer.SoundEffects.TOAD1)

                    # Start light strip pattern
                    box = BOXES[box_no]
                    multiseg = MultiSegment(self.grid, box[0], box[1], box[2], box[3], flipped_segs=(box[0], box[3]))
                    multiseg.set_rule(Rule().stripes((WHITE, OFF), 6).animate(16))

                if pressed_keys[BOX_KEYS[box_no]]:
                    self.set_mode(201, clear=True)

                # Print toad text letter by letter
                toad_letter = math.floor(time_elapsed * TOAD_TEXT_FRAMERATE)
                if toad_letter > len(TOAD_TEXT1):
                    self.screen.blit(self.font.render(TOAD_TEXT1, True, BLACK), (280, 250))
                    if toad_letter > len(TOAD_TEXT1) + len(TOAD_TEXT2):
                        self.screen.blit(self.font.render(TOAD_TEXT2, True, BLACK),
                                         (280, 280))
                        if toad_letter > len(TOAD_TEXT1) + len(TOAD_TEXT2) + len(TOAD_TEXT3):
                            self.screen.blit(
                                self.font.render(TOAD_TEXT3, True,
                                                 BLACK), (280, 310))
                        else:
                            self.screen.blit(self.font.render(TOAD_TEXT3[0:(toad_letter - len(TOAD_TEXT1) - len(TOAD_TEXT2))], True, BLACK), (280, 310))
                    else:
                        self.screen.blit(self.font.render(TOAD_TEXT2[0:(toad_letter - len(TOAD_TEXT1))], True, BLACK), (280, 280))
                    #
                    #
                else:
                    self.screen.blit(self.font.render(TOAD_TEXT1[0:toad_letter], True, BLACK), (280, 250))

            elif self.mode == 201:
                box_no = TUTORIAL_BOXES[1]

                if not self.mode_initialized:
                    # Render toad GUI
                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_toad, (60, 200))

                    # Play toad sound
                    self.sound_player.play_sound(SoundPlayer.SoundEffects.TOAD2)

                    # Start light strip pattern
                    box = BOXES[box_no]
                    multiseg = MultiSegment(self.grid, box[0], box[1], box[2], box[3], flipped_segs=(box[0], box[3]))
                    multiseg.set_rule(Rule().stripes((WHITE, OFF), 6).animate(16))

                # Print toad text letter by letter
                toad_letter = math.floor(time_elapsed * TOAD_TEXT_FRAMERATE)
                if toad_letter > len(TOAD_TEXT4):
                    self.screen.blit(self.font.render(TOAD_TEXT4, True, BLACK), (280, 250))
                else:
                    self.screen.blit(self.font.render(TOAD_TEXT4[0:toad_letter], True, BLACK), (280, 250))

                if pressed_keys[BOX_KEYS[box_no]]:
                    self.set_mode(202, clear=True)

            elif self.mode == 202:
                box_no = TUTORIAL_BOXES[2]

                if not self.mode_initialized:
                    # Render toad GUI
                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_toad, (60, 200))

                    # Play toad sound
                    self.sound_player.play_sound(SoundPlayer.SoundEffects.TOAD3)

                    # Start light strip pattern
                    box = BOXES[box_no]
                    multiseg = MultiSegment(self.grid, box[0], box[1], box[2], box[3], flipped_segs=(box[0], box[3]))
                    multiseg.set_rule(Rule().stripes((WHITE, OFF), 6).animate(16))

                # Print toad text letter by letter
                toad_letter = math.floor(time_elapsed * TOAD_TEXT_FRAMERATE)
                if toad_letter > len(TOAD_TEXT5):
                    self.screen.blit(self.font.render(TOAD_TEXT5, True, BLACK), (280, 250))
                else:
                    self.screen.blit(self.font.render(TOAD_TEXT5[0:toad_letter], True, BLACK), (280, 250))

                if pressed_keys[BOX_KEYS[box_no]]:
                    self.set_mode(203, clear=True)

            # Tutorial complete; prepare for real game
            elif self.mode == 203:
                if not self.mode_initialized:
                    # Render toad GUI
                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_toad, (60, 200))

                    # Play toad sound
                    self.sound_player.play_sound(SoundPlayer.SoundEffects.TOAD4)

                    # Play powerup stinger
                    self.sound_player.set_mode(SoundPlayer.Mode.WIN)

                # Print toad text letter by letter
                toad_letter = math.floor(time_elapsed * TOAD_TEXT_FRAMERATE)
                if toad_letter > len(TOAD_TEXT6):
                    self.screen.blit(self.font.render(TOAD_TEXT6, True, BLACK), (280, 250))
                else:
                    self.screen.blit(self.font.render(TOAD_TEXT6[0:toad_letter], True, BLACK), (280, 250))

                if time_elapsed > 4:
                    self.set_mode(300)

        # Modes 300-399 - gameplay
        elif self.mode <= 399:

            # Wait for user input on first row
            if self.mode == 300:
                if not self.mode_initialized:
                    # Play game music
                    self.sound_player.set_mode(SoundPlayer.Mode.PLAY)

                    # Initialize rules for side rails
                    self.grid.get_seg(0).set_rule(
                        Rule().stripes((RED, OFF, OFF, OFF, OFF, BLUE, OFF, OFF, OFF, OFF), 3).animate(30))
                    self.grid.get_seg(1).set_rule(
                        Rule().stripes((RED, OFF, OFF, OFF, OFF, BLUE, OFF, OFF, OFF, OFF), 3).animate(30))

                    self.star_start_time = time.time()

                # Display score
                self.screen.fill(BLACK)
                score_text = self.font.render("Stars collected: " + str(self.score) + " / " + str(self.max_score), True,
                                              WHITE)
                score_text = pygame.transform.scale(score_text, (380, 30))
                self.screen.blit(score_text, (200, 220))

                # Render stars
                frame = math.floor((time.time() - self.star_start_time) * STAR_FRAMERATE) % 32
                for i in range(10):
                    if self.active_squares[i] > 0:
                        self.screen.blit(self.image_star_array[frame],
                                         (self.pygame_rects[i][0], self.pygame_rects[i][1]))

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
                            multi_segment = MultiSegment(self.grid, *BOXES[chosen_square],
                                                         flipped_segs=[BOXES[chosen_square][0],
                                                                       BOXES[chosen_square][3]])
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
                    # Determine win/lose
                    if self.score / self.max_score > WIN_PERCENT:
                        self.set_mode(400, clear=True)
                    else:
                        self.set_mode(401, clear=True)

        # Modes 400-499: Final win sequence
        elif self.mode <= 499:
            # Mode 400 - win screen
            if self.mode == 400:
                if not self.mode_initialized:
                    self.sound_player.set_mode(SoundPlayer.Mode.WIN)
                    self.controller.flag_down()

                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_toad2, (100, 180))

                # Print toad text letter by letter
                toad_letter = math.floor(time_elapsed * TOAD_TEXT_FRAMERATE)
                if toad_letter > len(TOAD_TEXT7):
                    self.screen.blit(self.font.render(TOAD_TEXT7, True, BLACK), (380, 300))
                else:
                    self.screen.blit(self.font.render(TOAD_TEXT7[0:toad_letter], True, BLACK), (380, 300))

                if time_elapsed > 9:
                    self.reset_game()

            # Mode 401 - Bowser screen
            elif self.mode == 401:
                if not self.mode_initialized:
                    self.sound_player.set_mode(SoundPlayer.Mode.NONE)
                    self.sound_player.play_sound(self.sound_player.SoundEffects.BOWSER_LAUGH)
                    for i in range(42):
                        self.grid.get_seg(i).set_rule(Rule().fill(RED).blink(0.15, 0.15).fade_out(1, 1))
                    self.bowser_start_time = time.time()

                # Draw bowser
                frame = math.floor((time.time() - self.bowser_start_time) * BOWSER_FRAMERATE)
                if frame < 0:
                    frame = 0
                if frame > 61:
                    frame = 61

                self.screen.blit(self.image_bowser_array[frame], (0, 0))

                if time_elapsed > 5:
                    if self.lives > 0:
                        self.lives -= 1
                        self.set_mode(402)  # One-up screen
                    else:
                        self.set_mode(403)  # Game over

            # Mode 402 - one-up screen
            elif self.mode == 402:
                if not self.mode_initialized:
                    self.sound_player.play_sound(SoundPlayer.SoundEffects.ONE_UP)
                    self.screen.fill(WHITE)
                    self.screen.blit(self.image_oneup, (250, 50))
                    life_text = self.font.render("You got a one-up! You can do it!", True, BLACK)
                    life_text = pygame.transform.scale(life_text, (600, 50))
                    self.screen.blit(life_text, (100, 380))

                    self.controller.mushroom_up()

                    MultiSegment(self.grid, *ALL_SEGS).set_rule(Rule().fill(GREEN).blink(0.5, 0.5, 0))

                if time_elapsed > 5:
                    # Reset game stats
                    self.score = 0
                    self.max_score = 0
                    self.square_count = 0
                    self.active_squares = {i: -1 for i in range(10)}

                    self.controller.mushroom_down()
                    self.set_mode(300)

            # Mode 403 - game over mode
            elif self.mode == 403:
                if not self.mode_initialized:
                    self.sound_player.set_mode(SoundPlayer.Mode.LOSE)
                    self.screen.fill(BLACK)
                    self.screen.blit(self.image_game_over, (100, 120))

                if time_elapsed > 8:
                    self.reset_game()

        # Add cloud overlay
        self.screen.blit(self.image_overlay, (0, 0))
        pygame.display.update()

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
        self.animation_start_time = time.time()
        self.square_count = 0
        self.active_squares = {i: -1 for i in range(10)}
        self.score = 0
        self.max_score = 0
        self.lives = 1
        self.bowser_start_time = 0

        self.controller.mushroom_down()
        self.controller.flag_up()
