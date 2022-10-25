# TODO: Use polymorphism: Create interface 'Mode' and have game.py call its methods.
# Implement Mode as all of the different modes in separate Python files, i.e. 401, 402, etc.

import math, pathlib, time

import pygame

from all_modes import *
from colors import *
from controller import MultiSegment
from rule import Rule, Mode
from settings import *


# Controls the game logic and switching between modes.
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
        self.mode = Mode101(control, grid, screen)

        # Variables changed during gameplay
        self.square_count = 0
        self.active_squares = {i: -1 for i in range(10)}
        self.score = 0
        self.max_score = 0
        self.lives = 1
        self.star_start_time = 0
        self.bowser_start_time = 0

        # Initialize images for Pygame
        self.image_toad = pygame.image.load(str(IMAGE_DIR / 'toad.png')).convert()
        self.image_toad = pygame.transform.scale(self.image_toad, (360, 400))
        self.image_game_over = pygame.image.load(str(IMAGE_DIR / 'game_over.jpeg')).convert()
        self.image_game_over = pygame.transform.scale(self.image_game_over, (1300, 600))
        self.image_star_array = {}
        for i in range(32):
            star_img = pygame.image.load(str(IMAGE_DIR / ('star/frame_%02d_delay-0.06s.gif' % i))).convert()
            self.image_star_array[i] = pygame.transform.scale(star_img, (RECT_SIZE, RECT_SIZE))
        self.image_bowser_array = {}
        for i in range(62):
            bowser_img = pygame.image.load(str(IMAGE_DIR / ('bowser/%03d.png' % i))).convert()
            bowser_img = pygame.transform.scale(bowser_img, WINDOW_SIZE)
            self.image_bowser_array[i] = bowser_img

        # Initialize text for Pygame
        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", 50)
        self.toad_text1 = self.font.render("Hi! I need your help to collect the power", True, BLACK)
        self.toad_text2 = self.font.render("stars! Step on the square to start!", True, BLACK)
        self.toad_text3 = self.font.render("Great! Keep it up!", True, BLACK)
        self.toad_text4 = self.font.render("One square to go!", True, BLACK)
        self.toad_text5 = self.font.render("Great! Now get ready for the real game!", True, BLACK)

    def update(self, pressed_keys):
        """
        Called every frame - update the game state, LEDs, etc. based on input and timing.
        """

        self.mode = self.mode.update(pressed_keys)

        if False:
            # Mode 200-299 - tutorial mode
            if self.mode <= 299:
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
                        self.sound_player.set_mode(SoundPlayer.Mode.WIN)

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
                        self.grid.get_seg(0).set_rule(Rule().stripes((RED, OFF, OFF, OFF, OFF, BLUE, OFF, OFF, OFF, OFF), 3).animate(30))
                        self.grid.get_seg(1).set_rule(Rule().stripes((RED, OFF, OFF, OFF, OFF, BLUE, OFF, OFF, OFF, OFF), 3).animate(30))

                        self.star_start_time = time.time()

                    # Display score
                    self.screen.fill(BLACK)
                    score_text = self.font.render("Stars collected: " + str(self.score) + " / " + str(self.max_score), True, BLACK)
                    score_text = pygame.transform.scale(score_text, (600, 50))
                    self.screen.blit(score_text, (100, 70))

                    # Render stars
                    frame = math.floor((time.time() - self.star_start_time) * STAR_FRAMERATE) % 32
                    for i in range(10):
                        if self.active_squares[i] > 0:
                            self.screen.blit(self.image_star_array[frame], (self.pygame_rects[i][0], self.pygame_rects[i][1]))
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

                    pygame.display.update()

                    if time_elapsed > 5:
                        if self.lives > 0:
                            self.lives -= 1
                            self.set_mode(402) # One-up screen
                        else:
                            self.set_mode(403) # Game over

                # Mode 402 - one-up screen
                elif self.mode == 402:
                    if not self.mode_initialized:
                        pass
                        #self.screen.blit(self.image_) oneup

                # Mode 403 - game over mode
                elif self.mode == 403:
                    if not self.mode_initialized:
                        self.sound_player.set_mode(SoundPlayer.Mode.LOSE)
                        self.screen.fill(BLACK)
                        self.screen.blit(self.image_game_over, (300, 100))
                        pygame.display.update()

                    if time_elapsed > 5:
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
        self.lives = 1
        self.bowser_start_time = 0
