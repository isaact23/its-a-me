# A controller for all of the LED strips.
class Controller:
    def __init__(self, strip_sizes):
        """
        Create a controller with LED strips turned off.
        :param strip_sizes: a tuple listing the sizes of all connected LED strips (e.g. (150, 150, 50)).
        """
        self.strips = {}
        for i, size in enumerate(strip_sizes):
            self.strips[i] = self.LightStrip(self, size)

    def get_strip(self, strip):
        """
        :param strip: The index of the LightStrip to access.
        :return: The LightStrip object in the specified index.
        """
        return self.strips[strip]

    def write(self):
        """
        # Send all pixel data to LED strips.
        """
        for strip in self.strips:
            strip.write()

    # An LED strip.
    class LightStrip:
        def __init__(self, controller, size):
            """
            :param controller: The Controller object this LED strip is assigned to.
            :param size: The number of LEDs on this strip.
            """
            self.controller = controller
            self.size = size
            self.pixels = [(0, 0, 0)] * size
            # self.neopixel = neopixel.NeoPixel(board.D18, 150, auto_write=False)

        def get_segment(self, start, end):
            """
            Generate a Segment, which controls only some of the pixels on this LightStrip.
            :param start: The first pixel to control.
            :param end: The last pixel to control.
            :return: A Segment object with control over the specified pixels.
            """
            return self.Segment(self, start, end)

        def write(self):
            """
            Send pixel data to this LED strip.
            """
            pass

        # A segment of pixels, defined by the start and end pixels of one of the light strips.
        class Segment:
            def __init__(self, strip, start, end):
                """
                :param strip: The strip object this array lies on.
                :param start: The first pixel to activate
                :param end: The last pixel to activate
                """
                self.strip = strip
                self.start = start
                self.end = end
