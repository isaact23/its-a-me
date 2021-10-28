SEG_COUNT = 44


# A container class for all Segments that are part of the game. This class also has an emulator.
class Grid:
    def __init__(self, controller):
        self.controller = controller
        self.segments = []
        # Railings
        self.segments.append(controller.get_strip(0).get_segment(0, 50))
        self.segments.append(controller.get_strip(0).get_segment(50, 100))
        # Grid and pumpkins
        for i in range(2, SEG_COUNT):
            self.segments.append(controller.get_strip(0).get_segment(100 + i * 12, 100 + (i + 1) * 12))
        self.segments.append(controller.get_strip(0).get_segment(26, 46))


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
