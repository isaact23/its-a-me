SEG_COUNT = 44


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
        # Grid
        self.segments.append(strip.get_segment(160, 148))  # 2
        self.segments.append(strip.get_segment(148, 136))  # 3
        self.segments.append(strip.get_segment(172, 184))  # 4
        self.segments.append(strip.get_segment(112, 124))  # 5
        self.segments.append(strip.get_segment(280, 268))  # 6
        self.segments.append(strip.get_segment(232, 220))  # 7
        self.segments.append(strip.get_segment(292, 304))  # 8
        self.segments.append(strip.get_segment(196, 208))  # 9
        self.segments.append(strip.get_segment(364, 352))  # 10
        self.segments.append(strip.get_segment(352, 340))  # 11
        self.segments.append(strip.get_segment(376, 388))  # 12
        self.segments.append(strip.get_segment(316, 328))  # 13
        self.segments.append(strip.get_segment(472, 460))  # 14
        self.segments.append(strip.get_segment(436, 424))  # 15
        self.segments.append(strip.get_segment(484, 496))  # 16
        self.segments.append(strip.get_segment(400, 412))  # 17
        self.segments.append(strip.get_segment(556, 544))  # 18
        self.segments.append(strip.get_segment(544, 532))  # 19
        self.segments.append(strip.get_segment(568, 580))  # 20
        self.segments.append(strip.get_segment(508, 520))  # 21
        self.segments.append(strip.get_segment(160, 172))  # 22
        self.segments.append(strip.get_segment(196, 184))  # 23
        self.segments.append(strip.get_segment(100, 112))  # 24
        self.segments.append(strip.get_segment(136, 124))  # 25
        self.segments.append(strip.get_segment(280, 292))  # 26
        self.segments.append(strip.get_segment(268, 256))  # 27
        self.segments.append(strip.get_segment(232, 244))  # 28
        self.segments.append(strip.get_segment(220, 208))  # 29
        self.segments.append(strip.get_segment(364, 376))  # 30
        self.segments.append(strip.get_segment(400, 388))  # 31
        self.segments.append(strip.get_segment(304, 316))  # 32
        self.segments.append(strip.get_segment(340, 328))  # 33
        self.segments.append(strip.get_segment(472, 484))  # 34
        self.segments.append(strip.get_segment(460, 448))  # 35
        self.segments.append(strip.get_segment(436, 448))  # 36
        self.segments.append(strip.get_segment(424, 412))  # 37
        self.segments.append(strip.get_segment(556, 568))  # 38
        self.segments.append(strip.get_segment(592, 580))  # 39
        self.segments.append(strip.get_segment(496, 508))  # 40
        self.segments.append(strip.get_segment(532, 520))  # 41
        # Pumpkins
        for i in range(SEG_COUNT - 2, SEG_COUNT):
            self.segments.append(controller.get_strip(0).get_segment(100 + i * 12, 100 + (i + 1) * 12))


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

    def clear_rules(self, clear_grid=True, clear_railings=True, clear_pumpkins=True):
        """
        Erase rules for some Segments.
        :param clear_grid: Whether to clear the grid.
        :param clear_railings: Whether to clear railings.
        """
        if clear_grid or clear_railings or clear_pumpkins:
            for i, segment in enumerate(self.segments):
                if clear_railings and i < 2 or clear_grid and 1 < i < 42 or clear_pumpkins and i > 41:
                    segment.rule = None
