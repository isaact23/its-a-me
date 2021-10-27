import keyboard
import random
import time

import colors
import sounds
from colors import *
from controller import MultiSegment
from rule import Rule, Mode

# TODO: Review iosoft.blog
# https://iosoft.blog/2020/09/29/raspberry-pi-multi-channel-ws2812/

# Key definitions
KEY_START = 'space'
KEY_BOXES = ['left', 'right'] * 5

# Game constants
CASCADE_TIME = 0.8
REVEAL_BLINK_TIMES = (0.2, 0.18, 0.16, 0.14, 0.12)
WIN_TIME = 3.5
LOSE_TIME = 5
PUMPKIN_BLINK_TIME = 0.15

# An estimate of the length of each segment
SEG_WIDTH = 12

# Box definitions
BOXES = ((0, 12, 2, 13),
         (1, 13, 3, 14),
         (2, 15, 4, 16),
         (3, 16, 5, 17),
         (4, 18, 6, 19),
         (5, 19, 7, 20),
         (6, 21, 8, 22),
         (7, 22, 9, 23),
         (8, 24, 10, 25),
         (9, 25, 11, 26))
GRID = tuple(i for i in range(27))
RAILS = (27, 28)
ALL_SEGS = tuple(i for i in range(29))


def gen_correct_tiles():
    """
    Generate a 5 element array of bits, 0 representing left tile is correct, 1 means right is correct, for each row.
    """
    correct_tiles = [random.randint(0, 1) for i in range(5)]
    print("Correct tiles are", ["Left" if value == 0 else "Right" for value in correct_tiles])
    return correct_tiles


class Game:
    """
    Control all game logic for Glass Stepping Stones. There are multiple 'modes' which
    govern how rules are generated for lights and how input is handled.
    Mode 100 - attract
    Mode 200 - startup
    Mode 300 - gameplay
    Mode 400 - win
    """

    def __init__(self, control, grid, difficulty=0, kid_mode=True):
        """
        Initialize Game.
        :param control: LED controller.
        :param grid: Segment container class.
        """
        self.controller = control
        self.grid = grid
        self.difficulty = difficulty
        self.sound_player = sounds.SoundPlayer(kid_mode)
        self.box = -1
        self.mode = 100
        self.mode_initialized = False
        self.new_mode = False
        self.start_time = time.time()
        self.correct_tiles = gen_correct_tiles()

        # Variables used by update()
        self.row = 0
        self.undertale_count = 0
        self.started_scream = False

    def update(self):
        """
        Called every frame - update the game state, LEDs, etc. based on input and timing.
        """
        time_elapsed = time.time() - self.start_time
        self.new_mode = False

        # Mode 0-99 - testing purposes only
        if self.mode <= 99:
            # MultiSegment(self.grid, 12, 15, 18, 21, 24, 10, 11).set_rule(Rule().hue(60, 310, 0.1))
            # MultiSegment(self.grid, 12, 15, 18, 21, 24, 10, 11).set_rule(Rule().fill(RED).crop(40, 990))
            pass

        # Mode 100-199 - attract sequence
        elif self.mode <= 199:
            # If attract music is not playing, play it now.
            if not self.sound_player.get_busy():
                self.sound_player.attract_music()

            # On space press, move to stage 2 - start the game.
            if keyboard.is_pressed(KEY_START):
                self.set_mode(random.randint(200, 201), clear_all=True)
                self.sound_player.stop()
                self.undertale_count = 0

            elif self.mode == 100:
                if not self.mode_initialized:
                    # Railings are red/orange moving stripes in intro
                    self.grid.get_seg(27).set_rule(Rule().stripes((RED, ORANGE), width=8).animate(10).fade_in(2, 1))
                    self.grid.get_seg(28).set_rule(Rule().stripes((RED, ORANGE), width=8).animate(10).fade_in(2, 1))
                    self.grid.get_seg(29).set_rule(Rule().hue_wave(-120, 30, frequency=1, mode=Mode.TIME))
                    self.grid.get_seg(30).set_rule(Rule().stripes((MAGENTA, BLACK), 3).animate(10))
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
                    multi_seg = MultiSegment(self.grid, 12, 2, 16, 4, 18, 21, 24, 10, 11, 26,
                                             9, 22, 7, 20, 17, 14, 1, 0,
                                             flipped_segs=(4, 26, 9, 22, 20, 17, 14, 1, 0))
                    multi_seg.set_rule(Rule().fill(WHITE, -15, 0).animate(100))
                if time_elapsed > 5:
                    self.set_mode(103)

            elif self.mode == 103:
                if not self.mode_initialized:
                    multi_segs = []
                    multi_segs.append(MultiSegment(self.grid, 12, 15, 18, 21, 24, 10, 11))
                    multi_segs.append(MultiSegment(self.grid, 8, 25))
                    multi_segs.append(MultiSegment(self.grid, 6, 22, 9, 26))
                    multi_segs.append(MultiSegment(self.grid, 4, 19, 7, 23))
                    multi_segs.append(MultiSegment(self.grid, 2, 16, 5, 20))
                    multi_segs.append(MultiSegment(self.grid, 0, 13, 3, 17))
                    multi_segs.append(MultiSegment(self.grid, 1, 14))

                    for i, multi_seg in enumerate(multi_segs):
                        rule = Rule().hue_linear(5).fade_in(1, 0).fade_out(1, 5).animate(40)
                        if i == 1:
                            rule.offset(SEG_WIDTH * 4)
                        if i == 2:
                            rule.offset(SEG_WIDTH * 3)
                        if i == 3:
                            rule.offset(SEG_WIDTH * 2)
                        if i == 4:
                            rule.offset(SEG_WIDTH)
                        if i == 6:
                            rule.offset(SEG_WIDTH)

                        multi_seg.set_rule(rule)
                if time_elapsed > 7:
                    self.set_mode(104)

            elif self.mode == 104:
                if not self.mode_initialized:
                    MultiSegment(self.grid, 12, 15, 18, 21, 24, 10, 11, 26, 23, 20, 17, 14, 1, 0,
                                 flipped_segs=(26, 23, 20, 17, 14, 1, 0)).set_rule(
                        Rule().stripes((RED, ORANGE, YELLOW), 12).animate(30).fade_in(1, 0).fade_out(1, 5)
                    )
                if time_elapsed > 7:
                    self.set_mode(105)

            elif self.mode == 105:
                if not self.mode_initialized:
                    width = 6
                    speed = 50
                    MultiSegment(self.grid, 19, 22, 25, 10, 24, 8, 6, 18, 4, flipped_segs=(10, 24, 6, 18)).set_rule(
                        Rule().stripes((WHITE, BLACK), width).crop(-200, 0).animate(speed)
                    )
                    MultiSegment(self.grid, 11, 26, 9, 7, 20, 5, flipped_segs=(26, 9, 20, 5)).set_rule(
                        Rule().stripes((WHITE, BLACK), width).crop(-200, 0).offset(SEG_WIDTH * 3).animate(speed)
                    )
                    MultiSegment(self.grid, 16, 13, 0, 12, 2, flipped_segs=(16, 13, 0)).set_rule(
                        Rule().stripes((WHITE, BLACK), width).crop(-200, 0).animate(speed)
                    )
                    MultiSegment(self.grid, 1, 14, 3, flipped_segs=(3,)).set_rule(
                        Rule().stripes((WHITE, BLACK), width).crop(-200, 0).offset(SEG_WIDTH * 2).animate(speed)
                    )
                if time_elapsed > 9:
                    self.set_mode(101)

        # Mode 200-299 - transition to game
        elif self.mode <= 299:
            if self.mode == 200:
                if not self.mode_initialized:
                    MultiSegment(self.grid, 10, 11, 24, 25, 26, 8, 9).set_rule(
                        Rule().fill(WHITE).fade_in(0, 0).fade_out(1, 2))
                    MultiSegment(self.grid, 21, 6, 22, 7, 23).set_rule(
                        Rule().fill(WHITE).fade_in(0, CASCADE_TIME).fade_out(1, 2 + CASCADE_TIME))
                    MultiSegment(self.grid, 18, 4, 19, 5, 20).set_rule(
                        Rule().fill(WHITE).fade_in(0, CASCADE_TIME * 2).fade_out(1, 2 + CASCADE_TIME * 2))
                    MultiSegment(self.grid, 15, 2, 16, 3, 17).set_rule(
                        Rule().fill(WHITE).fade_in(0, CASCADE_TIME * 3).fade_out(1, 2 + CASCADE_TIME * 3))
                    MultiSegment(self.grid, 12, 0, 13, 1, 14).set_rule(
                        Rule().fill(WHITE).fade_in(0, CASCADE_TIME * 4).fade_out(1, 2 + CASCADE_TIME * 4))

                if self.undertale_count < 5 and time_elapsed > self.undertale_count * CASCADE_TIME:
                    self.sound_player.play(sounds.UNDERTALE)
                    self.undertale_count += 1
                if time_elapsed > 7:
                    self.set_mode(300)

            elif self.mode == 201:
                if not self.mode_initialized:
                    speed = 80
                    interval = 0.9
                    self.sound_player.play(sounds.GLRL_ONCE)
                    self.grid.get_seg(25).set_rule(
                        Rule().fill(RED, -1000, 0).animate(speed / 3).flip()
                    )
                    MultiSegment(self.grid, 10, 24, 8, flipped_segs=(10, 24)).set_rule(
                        Rule().fill(RED, -1000, 0).animate(speed)
                    )
                    MultiSegment(self.grid, 11, 26, 9, flipped_segs=(26, 9)).set_rule(
                        Rule().fill(RED, -1000, 0).animate(speed)
                    )
                    self.grid.get_seg(22).set_rule(
                        Rule().fill(RED, -1000, -interval * speed * 0.5).animate(speed / 2).flip()
                    )
                    MultiSegment(self.grid, 21, 6, flipped_segs=(21,)).set_rule(
                        Rule().fill(RED, -1000, -interval * speed).animate(speed)
                    )
                    MultiSegment(self.grid, 23, 7, flipped_segs=(23, 7)).set_rule(
                        Rule().fill(RED, -1000, -interval * speed).animate(speed)
                    )
                    self.grid.get_seg(19).set_rule(
                        Rule().fill(RED, -1000, -interval * speed).animate(speed / 2).flip()
                    )
                    MultiSegment(self.grid, 18, 4, flipped_segs=(18,)).set_rule(
                        Rule().fill(RED, -1000, -interval * speed * 2).animate(speed)
                    )
                    MultiSegment(self.grid, 20, 5, flipped_segs=(20, 5)).set_rule(
                        Rule().fill(RED, -1000, -interval * speed * 2).animate(speed)
                    )
                    self.grid.get_seg(16).set_rule(
                        Rule().fill(RED, -1000, -interval * speed * 1.5).animate(speed / 2).flip()
                    )
                    MultiSegment(self.grid, 15, 2, flipped_segs=(15,)).set_rule(
                        Rule().fill(RED, -1000, -interval * speed * 3).animate(speed)
                    )
                    MultiSegment(self.grid, 17, 3, flipped_segs=(17, 3)).set_rule(
                        Rule().fill(RED, -1000, -interval * speed * 3).animate(speed)
                    )
                    self.grid.get_seg(13).set_rule(
                        Rule().fill(RED, -1000, -interval * speed * 2).animate(speed / 2).flip()
                    )
                    MultiSegment(self.grid, 12, 0, flipped_segs=(12,)).set_rule(
                        Rule().fill(RED, -1000, -interval * speed * 4).animate(speed)
                    )
                    MultiSegment(self.grid, 14, 1, flipped_segs=(14, 1)).set_rule(
                        Rule().fill(RED, -1000, -interval * speed * 4).animate(speed)
                    )

                if time_elapsed > 4.75:
                    self.set_mode(202)

            elif self.mode == 202:
                if not self.mode_initialized:
                    MultiSegment(self.grid, *ALL_SEGS).set_rule(
                        Rule().fill(GREEN).fade_out(1, 2)
                    )
                if time_elapsed > 3.5:
                    self.set_mode(300, clear_grid=True, clear_railings=True)

        # Modes 300-399 - gameplay
        elif self.mode <= 399:
            # Wait for user input on first row
            if self.mode == 300:
                if not self.mode_initialized:
                    # Determine winning changes
                    winning_chance = self.get_winning_chance()
                    if winning_chance < 0.0001:
                        print("Current chance of winning is negligible.")
                    elif winning_chance > 0.9999:
                        print("Current chance of winning is quite high.")
                    else:
                        percent_chance = str(round(winning_chance * 100, 2)) + "%"
                        print("Current chance of winning is", percent_chance)

                    # Initialize blinking boxes
                    tempo = self.sound_player.choose_music()
                    left_box = self.row * 2
                    right_box = left_box + 1
                    blink_on = 30 / tempo
                    blink_off = blink_on
                    left_segs = [box for i, box in enumerate(BOXES[left_box]) if i != 3]
                    right_segs = [box for i, box in enumerate(BOXES[right_box]) if i != 1]
                    MultiSegment(self.grid, *left_segs).set_rule(
                        Rule().fill(WHITE).blink(
                            blink_on, blink_on + blink_off * 2))
                    MultiSegment(self.grid, *right_segs).set_rule(
                        Rule().fill(WHITE).blink(
                            blink_on, blink_on + blink_off * 2,
                            start_time=time.time() - blink_on - blink_off))
                    self.grid.get_seg(self.row * 3 + 13).set_rule(
                        Rule().fill(WHITE).blink(blink_on, blink_off))

                    # Initialize railings
                    self.grid.get_seg(27).set_rule(
                        Rule().stripes((RED, GREEN, BLUE, WHITE), 1).animate(3)
                    )
                    self.grid.get_seg(28).set_rule(
                        Rule().stripes((RED, GREEN, BLUE, WHITE), 1).animate(3)
                    )

                    # Initialize pumpkins
                    self.grid.get_seg(29).set_rule(Rule().hue_linear(15, mode=Mode.PIXEL).animate(10))
                    self.grid.get_seg(30).set_rule(Rule().hue_linear(15, mode=Mode.PIXEL).animate(10))

                # Left box
                if keyboard.is_pressed(KEY_BOXES[self.row * 2]):
                    self.set_mode(301, clear_grid=True)
                    self.box = self.row * 2
                # Right box
                elif keyboard.is_pressed(KEY_BOXES[self.row * 2 + 1]):
                    self.set_mode(301, clear_grid=True)
                    self.box = self.row * 2 + 1

            # If blinking,
            elif self.mode == 301:
                if not self.mode_initialized:
                    self.sound_player.stop()
                    MultiSegment(self.grid, *BOXES[self.box]).set_rule(
                        Rule().fill(BLUE).blink(REVEAL_BLINK_TIMES[self.row], REVEAL_BLINK_TIMES[self.row]))

                if time_elapsed > 2:
                    if self.is_tile_correct():
                        self.set_mode(302)  # Win
                    else:
                        self.set_mode(303)  # Lose

            # If winning,
            elif self.mode == 302:
                if not self.mode_initialized:
                    self.sound_player.correct()
                    self.correct_lights(self.box)

                if time_elapsed > WIN_TIME:
                    if self.row == 4:
                        self.set_mode(400, clear_grid=True, clear_railings=True)
                    else:
                        self.set_mode(300, clear_grid=True, clear_railings=True)  # Next round
                        self.row += 1

            # If losing,
            elif self.mode == 303:
                if not self.mode_initialized:
                    self.sound_player.wrong()
                    self.wrong_lights(self.box)

                if time_elapsed > 0.5 and not self.started_scream:
                    self.sound_player.scream()
                    self.started_scream = True
                if time_elapsed > LOSE_TIME:
                    self.reset_game()

        # Modes 400-499: Final win sequence
        elif self.mode <= 499:
            if not self.mode_initialized:
                print("The player has won. On to the next game!")
                self.sound_player.win()
                MultiSegment(self.grid, 12, 15, 18, 21, 24).set_rule(Rule().hue_wave(120, 240, 0.4, Mode.PIXEL).animate(20).fade_out(2, 6))
                MultiSegment(self.grid, 13, 16, 19, 22, 25).set_rule(Rule().hue_wave(120, 240, 0.4, Mode.PIXEL).animate(20).fade_out(2, 6))
                MultiSegment(self.grid, 14, 17, 20, 23, 26).set_rule(Rule().hue_wave(120, 240, 0.4, Mode.PIXEL).animate(20).fade_out(2, 6))
                MultiSegment(self.grid, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11).set_rule(Rule().hue_wave(120, 240, 2, Mode.TIME).fade_out(2, 6))
                self.grid.get_seg(27).set_rule(Rule().hue_wave(120, 240, 0.8).animate(10).fade_out(2, 6))
                self.grid.get_seg(28).set_rule(Rule().hue_wave(120, 240, 0.8).animate(10).fade_out(2, 6))
                self.grid.get_seg(29).set_rule(Rule().stripes((GREEN, BLACK), 3).animate(15).fade_out(2, 6))
                self.grid.get_seg(30).set_rule(Rule().stripes((GREEN, BLACK), 3).animate(-15).fade_out(2, 6))
            if time_elapsed > 9:
                self.reset_game()

        # If we just initialized, prevent re-initialization on next update cycles.
        if not self.mode_initialized and not self.new_mode:
            self.mode_initialized = True

    def correct_lights(self, box):
        """
        Set up light display if a player lands on a correct box.
        :param box: The ID of the correct box.
        """
        self.correct_lights1(box)

    def correct_lights1(self, box):
        """
        Correct light show 1.
        :param box: Correct box ID.
        """
        MultiSegment(self.grid, *ALL_SEGS).set_rule(
            Rule().stripes((GREEN, WHITE), 3).animate(12).fade_out(1, WIN_TIME - 1.5))
        MultiSegment(self.grid, *BOXES[box]).set_rule(
            Rule().fill(GREEN).fade_out(1, WIN_TIME - 1.5))

        bt = PUMPKIN_BLINK_TIME
        self.grid.get_seg(29).set_rule(
            Rule().fill(GREEN).blink(bt, bt, start_time=time.time() + bt).fade_out(1, WIN_TIME - 1.5)
        )
        self.grid.get_seg(30).set_rule(
            Rule().fill(GREEN).blink(bt, bt).fade_out(1, WIN_TIME - 1.5)
        )

    def wrong_lights(self, box):
        """
        Set up light display if a player lands on a wrong box.
        :param box: The ID of the wrong box.
        """
        self.wrong_lights1(box)

    def wrong_lights1(self, box):
        """
        Wrong light show 1.
        :param box: Wrong box ID.
        """
        MultiSegment(self.grid, *ALL_SEGS, continuous=False).set_rule(
            Rule().stripes((RED, OFF), 10).crop(-30, 200).animate(12))
        MultiSegment(self.grid, *BOXES[box], flipped_segs=(BOXES[0][0], BOXES[0][3])).set_rule(
            Rule().stripes((RED, OFF), 3).animate(10).fade_out(1.2, 2.5))

        bt = PUMPKIN_BLINK_TIME
        self.grid.get_seg(29).set_rule(
            Rule().fill(RED).blink(bt, bt, start_time=time.time() + bt).fade_out(1.2, 2.5)
        )
        self.grid.get_seg(30).set_rule(
            Rule().fill(RED).blink(bt, bt).fade_out(1.2, 2.5)
        )

    def is_tile_correct(self):
        """
        Determine if the tile a player stepped on is correct (i.e. won't break)
        :return: True if the tile didn't break.
        """
        tile = self.box % 2  # 0 if left, 1 if right
        correct = self.correct_tiles[self.row]

        # Calculate chance of something going wrong.
        power = 2 ** abs(self.difficulty)
        anomaly_chance = 1
        if power != 0:
            anomaly_chance = (power - 1) / power

        # Determine if tile is correct, then determine if the chance will adjust the outcome.
        if tile == correct:
            if self.difficulty > 0 and random.random() <= anomaly_chance:
                print("Correct tile, but it broke anyway. Difficulty =", self.difficulty)
                return False
            else:
                print("Correct tile!")
                return True
        else:
            if self.difficulty < 0 and random.random() <= anomaly_chance:
                print("Wrong tile, but it didn't break. Difficulty =", self.difficulty)
                return True
            else:
                print("Wrong tile!")
                return False

    def get_winning_chance(self):
        """
        :return: Current chance of winning as a percentage.
        """
        # Determine chance of anomaly
        power = 2 ** abs(self.difficulty)
        anomaly_chance = 1
        if power != 0:
            anomaly_chance = (power - 1) / power

        # Determine chance of winning overall
        turns_remaining = 5 - self.row
        if self.difficulty > 0:
            row_chance = 0.5 - (0.5 * anomaly_chance)
        else:
            row_chance = 0.5 + (0.5 * anomaly_chance)
        overall_chance = row_chance ** turns_remaining

        return overall_chance

    def set_mode(self, mode, clear_all=False, clear_grid=False, clear_railings=False, clear_pumpkins=False):
        """
        Prepare for a new mode.
        """
        if clear_all:
            clear_grid = True
            clear_railings = True
            clear_pumpkins = True
        self.mode = mode
        self.start_time = time.time()
        self.mode_initialized = False
        self.new_mode = True
        self.grid.clear_rules(clear_grid, clear_railings, clear_pumpkins)
        print("Set mode to", mode)

    def reset_game(self):
        """
        Re-initialize the game for a new round.
        """
        self.set_mode(100, clear_grid=True, clear_railings=True)
        self.row = 0
        self.box = -1
        self.correct_tiles = gen_correct_tiles()
        self.undertale_count = 0
        self.started_scream = False
