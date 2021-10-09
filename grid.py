# A container class for all Segments that are part of the game. This class also has an emulator.
class Grid:
    def __init(self, controller):
        self.a1 = controller.get_strip(0).get_segment(0, 20) # Front left horizontal
        self.a2 = controller.get_strip(1).get_segment(50, 100) # Front right horizontal
        self.b1 = None # Left vertical
        self.b2 = None # Middle vertical
        self.b3 = None # Right vertical
        self.c1 = None # The pattern repeats for the remainder of the grid.
        self.c2 = None
        self.d1 = None
        self.d2 = None
        self.d3 = None
        self.e1 = None
        self.e2 = None
        self.f1 = None
        self.f2 = None
        self.f3 = None
        self.g1 = None
        self.g2 = None
        self.h1 = None
        self.h2 = None
        self.h3 = None
        self.k1 = None
        self.k2 = None
        self.l1 = None # Left rope
        self.r1 = None # Right rope
