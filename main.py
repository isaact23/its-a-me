# Squid Game - Glass Stepping Stones
# Code for LED strips, sound control, camera, etc.

# import neopixel, board
import colorsys, random, time, math
import colors
from controller import Controller, LightStrip
from grid import Grid
from emulator import Emulator

def main():
    controller = Controller((150, 150, 50))
    grid = Grid(controller)
    emulator = Emulator(grid)
    seg1 = controller.get_strip(0).get_segment(20, 70)
    print(seg1.start)


if __name__ == "__main__":
    main()
