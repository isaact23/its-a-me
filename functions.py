# Several functions that generate lambdas, passable to Segments and LightStrips.

import time


# TODO: Make this object-oriented so we can chain methods rather than nesting them

def fill(color):
    """
    :param color: The color to set all pixels to.
    :return: A lambda 'fill' function.
    """

    def f(**kwargs):
        return color

    return f


def stripes(colors, width):
    """
    Generate stripes with alternating colors.
    :param colors: The colors to choose from.
    :param width: The width of each stripe.
    :return: A lambda stripe function.
    """

    def f(**kwargs):
        if kwargs['pixel'] is None:
            raise RuntimeError("pixel argument missing")
        return colors[(kwargs['pixel'] // width) % len(colors)]

    return f


# Function modifiers - pass a function, return a modified version of the original.

def flip(f):
    """
    Flip the original function, so the last pixel is in the place of the first pixel, etc.
    :param f: The function to flip.
    :return: The flipped function.
    """

    def f2(**kwargs):
        new_args = kwargs
        new_args['pixel'] = new_args['seg_size'] - new_args['pixel']
        return f(**new_args)

    return f2


def animate(f, speed):
    """
    Animate the original function, causing it to move over time.
    :param f: The function to modify.
    :param speed: The speed at which the function should move.
    :return: The modified function.
    """

    start_time = time.time()

    def f2(**kwargs):
        new_args = kwargs
        new_args['pixel'] += round((time.time() - start_time) * speed)
        return f(**new_args)

    return f2

# Others - fade, ripple, etc.
