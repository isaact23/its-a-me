# A container class for all Segments that are part of the game. This class also has an emulator.
class Grid:
    def __init__(self, controller):
        self.controller = controller
        self.segments = [
            None, None,
            controller.get_strip(0).get_segment(0, 20),  # Front left horizontal
            controller.get_strip(1).get_segment(50, 100),  # Front right horizontal
        ]
        for i in range(20):
            self.segments.append(None)

    def use_func(self):
        """
        Tell all segments to update LEDs as per their functions.
        """
        for segment in self.segments:
            segment.use_func()
        self.controller.write()
