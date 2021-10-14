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

    def fill(self, color, start=None, end=None):
        """
        Set LEDs in a range to the same color.
        :param color: The color to set all pixels to.
        :param start: The first pixel to modify (inclusive, optional).
        :param end: The last pixel to modify (exclusive, optional).
        """

        def f(**kwargs):
            if start is None or end is None or start <= kwargs['pixel'] < end:
                return color
            return 0, 0, 0

        self.func_chain.append(f)
        return self

    def stripes(self, colors, width):
        """
        Generate stripes with alternating colors.
        :param colors: The colors to choose from.
        :param width: The width of each stripe.
        """

        def f(**kwargs):
            if kwargs['pixel'] is None:
                raise RuntimeError("pixel argument missing")
            return colors[(kwargs['pixel'] // width) % len(colors)]

        self.func_chain.append(f)
        return self

    # Secondary rules - modify the existing Rule.

    def animate(self, speed):
        """
        Animate the original function, causing it to move over time.
        :param speed: The speed at which the function should move.
        """

        start_time = time.time()
        last_func = self.get_last_func()

        def f2(**kwargs):
            kwargs['pixel'] -= round((time.time() - start_time) * speed)
            return last_func(**kwargs)

        self.func_chain.append(f2)
        return self

    def fade_in(self, fade_time, delay):
        """
        Fade from black to the function color.
        :param fade_time: How long the fade effect should take.
        :param delay: Time in seconds to wait to fade in.
        """

        start_time = time.time()
        last_func = self.get_last_func()

        def f2(**kwargs):
            time_elapsed = time.time() - start_time
            if time_elapsed < delay:
                return 0, 0, 0
            full_color = last_func(**kwargs)
            if fade_time == 0 or time_elapsed > fade_time + delay:
                return full_color
            percent = (time.time() - delay - start_time) / fade_time
            new_color = round(full_color[0] * percent), round(full_color[1] * percent), round(full_color[2] * percent)
            return new_color

        self.func_chain.append(f2)
        return self

    def fade_out(self, fade_time, delay):
        """
        Fade from the function color to black.
        :param fade_time: How long the fade effect should take.
        :param delay: Time in seconds to wait to fade out.
        """

        start_time = time.time()
        last_func = self.get_last_func()

        def f2(**kwargs):
            time_elapsed = time.time() - start_time
            if time_elapsed > fade_time + delay:
                return 0, 0, 0
            full_color = last_func(**kwargs)
            if time_elapsed < delay:
                return full_color
            percent = 1 - ((time.time() - delay - start_time) / fade_time)
            new_color = round(full_color[0] * percent), round(full_color[1] * percent), round(full_color[2] * percent)
            return new_color

        self.func_chain.append(f2)
        return self

    def flip(self):
        """
        Flip the original function, so the last pixel is in the place of the first pixel, etc.
        """

        last_func = self.get_last_func()

        def f2(**kwargs):
            kwargs['pixel'] = kwargs['seg_size'] - kwargs['pixel']
            return last_func(**kwargs)

        self.func_chain.append(f2)
        return self

    def offset(self, pixels):
        """
        Shift this Rule by a certain number of pixels.
        :param pixels: The number of pixels to shift.
        """

        last_func = self.get_last_func()

        def f2(**kwargs):
            kwargs['pixel'] += pixels
            return last_func(**kwargs)

        self.func_chain.append(f2)
        return self

    # Others - fade, ripple, etc.

    # Miscellaneous functions

    def get_last_func(self):
        """
        :return: The last function in the function chain.
        """
        return self.func_chain[-1]
