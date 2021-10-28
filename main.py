# Squid Game - Glass Stepping Stones
# Code for LED strips, sound control, camera, etc.

# TODO: Optimize! Profile Rule(), write() functions, etc.
# TODO: Add python console controls
# TODO: Make it so squares don't share sides

import fpstimer
import sys
import time

from controller import Controller
from grid import Grid
from emulator import Emulator
from game import Game

FRAMERATE = 60
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

    control = Controller((1000,))
    grid = Grid(control)
    game = Game(control, grid, difficulty=DIFFICULTY, kid_mode=KID_MODE)

    # Begin emulation
    if USE_EMULATOR:
        emulator = Emulator(grid)

    # Frames per second stuff
    timer = fpstimer.FPSTimer(FRAMERATE)
    start_time = time.time()
    frame_count = 0

    while True:
        time1 = time.perf_counter()
        game.update()  # Update game logic
        time2 = time.perf_counter()
        grid.use_rule()  # Update colors
        time3 = time.perf_counter()
        control.write()  # Update LED strips
        if USE_EMULATOR:
            emulator.update()  # Update GUI
        time4 = time.perf_counter()
        # timer.sleep()  # 60 FPS
        frame_count += 1
        """print("Game update time:", time2 - time1)
        print("Use rule time:", time3 - time2)
        print("Write time:", time4 - time3)"""

        # Report FPS
        if REPORT_FPS:
            time_elapsed = time.time() - start_time
            if time_elapsed > 1.0:
                print("FPS: ", frame_count / time_elapsed)
                start_time = time.time()
                frame_count = 0


if __name__ == "__main__":
    main()
