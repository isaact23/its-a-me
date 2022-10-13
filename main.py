# It's a me
# Halloween 2022 project by Andy Thompson and Isaac Thompson

import faulthandler
faulthandler.enable()

import fpstimer
import sys

from controller import Controller
from grid import Grid
from emulator import Emulator
from game import Game

FRAMERATE = 60
USE_EMULATOR = True


def main():
    print("Python version:", sys.version)
    if USE_EMULATOR:
        print("Using emulator.")
    else:
        print("Emulator disabled.")

    control = Controller((580,))
    grid = Grid(control)
    game = Game(control, grid)

    # Begin emulation
    if USE_EMULATOR:
        emulator = Emulator(grid)

    # Framerate maintainer
    timer = fpstimer.FPSTimer(FRAMERATE)

    while True:
        game.update()  # Update game logic
        grid.use_rule()  # Update LED colors
        control.write()  # Update LED strips
        if USE_EMULATOR:
            emulator.update()  # Update GUI
        
        timer.sleep()  # 60 FPS
        print("RUNNING")


if __name__ == "__main__":
    main()
