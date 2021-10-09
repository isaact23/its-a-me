# Several functions that generate lambdas, passable to Segments and LightStrips.

import time


def fill(color):
    """
    :param color: The color to set all pixels to.
    """

    def f(**kwargs):
        return color

    return f


def stripes(colors):
    pass


# Function modifiers - pass a function, return a modified version of the original.

def flip(f):
    pass


def animate(f):
    pass
