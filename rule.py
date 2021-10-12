import time


class Rule:
    """
    Class passable to Segments and LightStrips that determines LED colors at runtime.
    """

    def __init__(self):
        self.func_chain = []  # Every time a new function is generated, append it here.

    def __call__(self, **kwargs):
        """
        Evaluate this rule based on kwargs.
        :param kwargs: Properties needed to determine color, e.g. led index, segment size, etc.
        :return: The generated color.
        """
        if len(self.func_chain) == 0:
            return 0, 0, 0
        return self.func_chain[-1](**kwargs)

    # Primary rules - these generate colors and don't modify any functions.

    def fill(self, color):
        """
        Set all LEDs to the same color.
        :param color: The color to set all pixels to.
        :return: This Rule object.
        """

        def f(**kwargs):
            return color

        self.func_chain.append(f)
        return self

    def stripes(self, colors, width):
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

        self.func_chain.append(f)
        return self

    # Secondary rules - modify the existing Rule.

    def flip(self):
        """
        Flip the original function, so the last pixel is in the place of the first pixel, etc.
        :return: The flipped function.
        """

        last_func = len(self.func_chain) - 1

        def f2(**kwargs):
            new_args = kwargs
            new_args['pixel'] = new_args['seg_size'] - new_args['pixel']
            return self.func_chain[last_func](**new_args)

        self.func_chain.append(f2)
        return self

    def animate(self, speed):
        """
        Animate the original function, causing it to move over time.
        :param speed: The speed at which the function should move.
        :return: The modified function.
        """

        start_time = time.time()
        last_func = len(self.func_chain) - 1

        def f2(**kwargs):
            new_args = kwargs
            new_args['pixel'] += round((time.time() - start_time) * speed)
            return self.func_chain[last_func](**new_args)

        self.func_chain.append(f2)
        return self

    # Others - fade, ripple, etc.
