# Squid Game - Glass Stepping Stones
# Code for LED strips, sound control, camera, etc.

import fpstimer
from controller import Controller
from grid import Grid
from emulator import Emulator
from game import Game


def main():
    control = Controller((20, 20, 2000, 20, 20, 20, 20, 20, 20, 20, 20))
    grid = Grid(control)
    game = Game(control, grid)

    # Begin emulation
    emulator = Emulator(grid)
    timer = fpstimer.FPSTimer(60)
    while True:
        game.update()  # Update game logic
        grid.use_rule()  # Update colors
        control.write()  # Update LED strips
        emulator.update()  # Update GUI
        timer.sleep()  # 60 FPS


if __name__ == "__main__":
    main()
