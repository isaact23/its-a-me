SEG_COUNT = 31


# A container class for all Segments that are part of the game. This class also has an emulator.
class Grid:
    def __init__(self, controller):
        self.controller = controller
        self.segments = [
            controller.get_strip(0).get_segment(0, 20),
            controller.get_strip(1).get_segment(0, 20)
        ]
        for i in range(SEG_COUNT - 2):
            self.segments.append(controller.get_strip(2).get_segment(i * 12, (i + 1) * 12))

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
        if clear_grid or clear_railings:
            for i, segment in enumerate(self.segments):
                if clear_grid and i < 27 or clear_railings and 26 < i < 29 or clear_pumpkins and i > 28:
                    segment.rule = None
