# It's a me
# Halloween 2022 project by Andy Thompson and Isaac Thompson

import fpstimer
import sys
#import faulthandler
#faulthandler.enable()

ENABLE_EMULATOR = True

import pygame

from controller import Controller
from grid import Grid
from game import Game
if ENABLE_EMULATOR:
    from emulator import Emulator

FRAMERATE = 60
PIXEL_COUNT = 580

# GUI settings
WINDOW_SIZE = (800, 600)


class ItsAMe():
    def __init__(self):
        print("Python version:", sys.version)

        # Initialize game logic and LED stuff
        self.control = Controller((PIXEL_COUNT,))  # LED Controller
        self.grid = Grid(self.control)                  # Container for all LED segments
        self.game = Game(self.control, self.grid)            # Game logic manager
        if ENABLE_EMULATOR:
            self.emulator = Emulator(self.grid)

        # Initialize FPS timer
        self.timer = fpstimer.FPSTimer(FRAMERATE)

        # Initialize Pygame (GUI / Sound)
        pygame.init()
                # TODO: Find source of colors being out of range
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        while(True):
            self.update()

    def update(self):
        self.game.update(pygame.key.get_pressed())  # Update game logic
        #print("Updated game")
        self.grid.use_rule()  # Update LED colors
        #print("Updated rule")
        self.control.write()  # Update LED strips
        #print("Updated strip")
        if ENABLE_EMULATOR:
            self.emulator.update()
        
        self.timer.sleep()  # 60 FPS


if __name__ == "__main__":
    its_a_me = ItsAMe() # Initialize the entire gosh diddly dang darn thing
