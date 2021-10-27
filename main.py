# Squid Game - Glass Stepping Stones
# Code for LED strips, sound control, camera, etc.

# TODO: Optimize!

import fpstimer
import sys
import time

from controller import Controller
from grid import Grid
from emulator import Emulator
from game import Game

USE_EMULATOR = False
KID_MODE = True
REPORT_FPS = False

# Set difficulty to 0 for a 50/50 shot for every row.
# Make more negative so the wrong tiles are less likely to break.
# Make more positive so the correct tiles are more likely to break.
# Difficulty change compounds quite dramatically so small changes are best (maybe 0.5 at a time)
DIFFICULTY = 0


def main():
    print("Python version:", sys.version)
    if USE_EMULATOR:
        print("Using emulator.")
    else:
        print("Emulator disabled.")
    if KID_MODE:
        print("Kid mode enabled - scary sounds shouldn't play. No guarantees of course. Phew glad I got that "
              "liability off my chest")
    else:
        print("Kid mode disabled - beware of scary sounds!")

    control = Controller((20, 20, 2000, 20, 1000))
    grid = Grid(control)
    game = Game(control, grid, difficulty=DIFFICULTY, kid_mode=KID_MODE)

    # Begin emulation
    if USE_EMULATOR:
        emulator = Emulator(grid)

    # Frames per second stuff
    timer = fpstimer.FPSTimer(60)
    start_time = time.time()
    frame_count = 0

    while True:
        game.update()  # Update game logic
        grid.use_rule()  # Update colors
        control.write()  # Update LED strips
        if USE_EMULATOR:
            emulator.update()  # Update GUI
        timer.sleep()  # 60 FPS
        frame_count += 1

        # Report FPS
        if REPORT_FPS:
            time_elapsed = time.time() - start_time
            if time_elapsed > 1.0:
                print("FPS: ", frame_count / time_elapsed)
                start_time = time.time()
                frame_count = 0


if __name__ == "__main__":
    main()
