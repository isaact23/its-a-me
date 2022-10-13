SEG_COUNT = 42


# A container class for all Segments that are part of the game. This class also has an emulator.
class Grid:
    def __init__(self, controller):
        self.controller = controller
        self.segments = []
        strip = controller.get_strip(0)
        # Flip RGB
        strip.flip_rgb(0, 100)
        # Railings
        self.segments.append(strip.get_segment(0, 50))  # 0
        self.segments.append(strip.get_segment(50, 100))  # 1
        # Grid
        for i in range(40):
            self.segments.append(strip.get_segment(100 + i * 12, 100 + (i + 1) * 12))


    def get_seg(self, segment):
        """
        Get one of the segments from this grid.
        :param segment: The segment index to get.
        :return: A Segment given by the index specified.
        :raises IndexError: When segment index is out of bounds.
        """
        if segment >= SEG_COUNT or segment < 0:
            raise IndexError("Segment index out of bounds")

        return self.segments[segment]

    def use_rule(self):
        """
        Tell all segments to update LEDs as per their functions.
        """
        for segment in self.segments:
            segment.use_rule()
        self.controller.write()

    def clear_rules(self):
        """
        Erase rules for all Segments.
        """
        for i, segment in enumerate(self.segments):
            segment.rule = None
