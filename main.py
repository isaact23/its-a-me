# Squid Game - Glass Stepping Stones
# Code for LED strips, sound control, camera, etc.

# import neopixel, board
import colorsys, random, math, fpstimer
from time import perf_counter
import colors
import rule
from controller import Controller, LightStrip
from grid import Grid
from emulator import Emulator
from rule import Rule


def main():
    controller = Controller((20, 20, 1000))
    grid = Grid(controller)
    grid.get_seg(7).set_rule(Rule().fill(colors.RED))
    grid.get_seg(4).set_rule(Rule().stripes((colors.RED, colors.BLUE), width=3).animate(15))
    grid.get_seg(12).set_rule(Rule().stripes(colors.USA, width=2).animate(-25))

    # Begin emulation
    emulator = Emulator(grid)
    timer = fpstimer.FPSTimer(60)
    i = 0
    while True:
        grid.use_rule()
        emulator.update()
        timer.sleep()


if __name__ == "__main__":
    main()
