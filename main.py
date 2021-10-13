# Squid Game - Glass Stepping Stones
# Code for LED strips, sound control, camera, etc.

# import neopixel, board
import colorsys, random, math, fpstimer
from time import perf_counter
import colors
import rule
from controller import Controller, LightStrip, MultiSegment
from grid import Grid
from emulator import Emulator
from rule import Rule


def main():
    control = Controller((20, 20, 2000, 20, 20, 20, 20, 20, 20, 20, 20))
    grid = Grid(control)
    grid.get_seg(7).set_rule(Rule().fill(colors.RED))
    grid.get_seg(4).set_rule(Rule().stripes((colors.RED, colors.BLUE), width=3).animate(15))
    grid.get_seg(12).set_rule(Rule().stripes(colors.USA, width=25).animate(10))
    grid.get_seg(15).set_rule(Rule().stripes(colors.USA, width=25).animate(10))
    grid.get_seg(18).set_rule(Rule().stripes(colors.USA, width=25).animate(10))
    grid.get_seg(21).set_rule(Rule().stripes(colors.USA, width=25).animate(10))
    grid.get_seg(24).set_rule(Rule().stripes(colors.USA, width=25).animate(10))
    grid.get_seg(27).set_rule(Rule().stripes(colors.MEXICO, width=3))
    grid.get_seg(28).set_rule(Rule().stripes(colors.MEXICO, width=3))
    orange = Rule().fill(colors.ORANGE)
    grid.get_seg(25).set_rule(orange)
    grid.get_seg(26).set_rule(orange)
    grid.get_seg(9).set_rule(orange)
    grid.get_seg(11).set_rule(orange)

    box1 = MultiSegment(grid, 1, 13, 3, 14)
    box1.set_rule(Rule().stripes(colors.RAINBOW, width=3))
    box1.use_rule()

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
