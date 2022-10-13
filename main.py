# It's a me
# Halloween 2022 project by Andy Thompson and Isaac Thompson

import fpstimer
import sys
import faulthandler
faulthandler.enable()

import pygame

from controller import Controller
from grid import Grid
#from emulator import Emulator
from game import Game

FRAMERATE = 60
PIXEL_COUNT = 580

class ItsAMe():
    def __init__(self):
        print("Python version:", sys.version)

        self.control = Controller((PIXEL_COUNT,))  # LED Controller
        self.grid = Grid(control)                  # Container for all LED segments
        self.game = Game(control, grid)            # Game logic manager

        self.timer = fpstimer.FPSTimer(FRAMERATE)

        while(True):
            self.update()

    def update(self):
        self.game.update()  # Update game logic
        print("Updated game")
        self.grid.use_rule()  # Update LED colors
        print("Updated rule")
        self.control.write()  # Update LED strips
        print("Updated strip")
        
        self.timer.sleep()  # 60 FPS
        

if __name__ == "__main__":
    its_a_me = ItsAMe() # Initialize the entire gosh diddly dang darn thing
