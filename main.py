# Squid Game - Glass Stepping Stones
# Code for LED strips, sound control, camera, etc.

# import neopixel, board
import colorsys, random, time, math
import colors
import functions
from controller import Controller, LightStrip
from grid import Grid
from emulator import Emulator


def main():
    controller = Controller((20, 20, 1000))
    grid = Grid(controller)
    seg = grid.get_segment(7)
    seg.set_func(functions.fill(colors.RED))
    seg.use_func()
    emulator = Emulator(grid)


if __name__ == "__main__":
    main()
