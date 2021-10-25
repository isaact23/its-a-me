# Squid Game - Glass Stepping Stones
# Code for LED strips, sound control, camera, etc.

import fpstimer
import sys
from time import perf_counter

from controller import Controller
from grid import Grid
from emulator import Emulator
from game import Game
import sounds

USE_EMULATOR = True

def main():
    print("Python version:", sys.version)
    if USE_EMULATOR:
        print("Using emulator.")
    else:
        print("Emulator disabled.")
    if sounds.KID_MODE:
        print("Kid mode enabled - scary sounds shouldn't play. No guarantees of course. Phew glad I got that "
              "liability off my chest")
    else:
        print("Kid mode disabled - beware of scary sounds!")

    control = Controller((20, 20, 2000, 20, 1000))
    grid = Grid(control)
    game = Game(control, grid)

    # Begin emulation
    emulator = None
    timer = fpstimer.FPSTimer(60)
    while True:
        time1 = perf_counter()
        game.update()  # Update game logic
        time2 = perf_counter()
        grid.use_rule()  # Update colors
        time3 = perf_counter()
        control.write()  # Update LED strips
        time4 = perf_counter()
        if USE_EMULATOR:
            if emulator is None:
                emulator = Emulator(grid)
            emulator.update()  # Update GUI
        if time4 == time3:
            time4 += 0.01
        #print("FPS Game update:", 1/(time2-time1), "Grid use rule:", 1/(time3-time2), "Control write:", 1/(time4-time3))
        timer.sleep()  # 60 FPS


if __name__ == "__main__":
    main()
