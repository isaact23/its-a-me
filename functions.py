# Several functions that generate lambdas, passable to Segments and LightStrips.

def fill(color):
    """
    :param color: The color to set all pixels to.
    """
    def f(**kwargs):
        return color

    return f
