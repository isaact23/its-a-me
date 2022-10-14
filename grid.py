SEG_COUNT = 42
BOX_SEGS = [
    (5, 4),
    (4, 3),
    (6, 7),
    (1, 2),
    (14, 13),
    (11, 10),
    (15, 16),
    (8, 9),
    (21, 20),
    (20, 19),
    (22, 23),
    (17, 18),
    (30, 29),
    (27, 26),
    (31, 32),
    (24, 25),
    (37, 36),
    (36, 35),
    (38, 39),
    (33, 34),

    (5, 6),
    (8, 7),
    (0, 1),
    (3, 2),
    (14, 15),
    (13, 12),
    (11, 12),
    (10, 9),
    (21, 22),
    (24, 23),
    (16, 17),
    (19, 18),
    (30, 31),
    (29, 28),
    (27, 28),
    (26, 25),
    (37, 38),
    (40, 39),
    (32, 33),
    (35, 34)
]

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
        self.segments.append(strip.get_segment(100, 50))  # 1
        # Box segments
        for seg in BOX_SEGS:
            self.segments.append(strip.get_segment(100 + seg[0] * 12, 100 + seg[1] * 12))
        # Grid
        #for i in range(40):
        #    self.segments.append(strip.get_segment(100 + i * 12, 99 + (i + 1) * 12))


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
