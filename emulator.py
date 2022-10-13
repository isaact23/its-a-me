import math
import tkinter as tk
import sys
from time import perf_counter

# Set constants
import grid

BOX_WIDTH = 80  # Width of each of the squares
MARGIN = 75  # Distance between outside of game and edge of window
RAILING_DIST = 75  # Distance between railing and tiles
BOX_SPACING = 20  # Distance between squares
CIRCLE_MARGIN = 0  # Distance between coordinates and first circle of each Segment=

LINE_WIDTH = 2
CIRCLE_SIZE = 7
RAIL_CIRCLE_SIZE = 9

# Determine window size
WINDOW_WIDTH = MARGIN * 2 + RAILING_DIST * 2 + BOX_WIDTH * 2 + BOX_SPACING
WINDOW_HEIGHT = MARGIN * 2 + BOX_WIDTH * 5 + BOX_SPACING * 4

# Generate railing coordinates
TL = (MARGIN, MARGIN)
BL = (MARGIN, MARGIN + BOX_WIDTH * 5 + BOX_SPACING * 4)
TR = (MARGIN + RAILING_DIST * 2 + BOX_WIDTH * 2 + BOX_SPACING, MARGIN)
BR = (MARGIN + RAILING_DIST * 2 + BOX_WIDTH * 2 + BOX_SPACING, MARGIN + BOX_WIDTH * 5 + BOX_SPACING * 4)

# Generate grid coordinates
coords = []
for y in range(10):
    for x in range(4):
        # Generate top left coordinate, then add on as needed
        coord = [MARGIN + RAILING_DIST, MARGIN + (BOX_WIDTH * 5) + (BOX_SPACING * 4)]
        coord[0] += BOX_WIDTH * (math.ceil(x / 2))
        coord[0] += BOX_SPACING * (x // 2)
        coord[1] -= BOX_WIDTH * (math.ceil(y / 2))
        coord[1] -= BOX_SPACING * (y // 2)

        coords.append(coord)


# Image generator for the current state of the light show.
class Emulator:
    def __init__(self, grid):
        self.grid = grid
        self.circles = {}  # LED circle objects, indexed by segments

        # Initialize window/canvas
        self.root = tk.Tk()
        self.root.title("Glass Stepping Stones")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.canvas = tk.Canvas(self.root, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

        self.canvas.pack()
        self.gen_circles()
        self.update()

    def gen_circles(self):
        """
        Create all circle objects representative of individual LEDs.
        """
        # Railings
        seg_length = (BOX_WIDTH * 5) + (BOX_SPACING * 4) - (CIRCLE_MARGIN * 2)
        for x in range(2):
            seg_id = x
            seg = self.grid.get_seg(seg_id)
            led_count = seg.size()
            led_space = seg_length / led_count
            if x == 0:
                origin = (MARGIN,
                          MARGIN + BOX_WIDTH * 5 + BOX_SPACING * 4)
            else:
                origin = (MARGIN + RAILING_DIST * 2 + BOX_WIDTH * 2 + BOX_SPACING,
                          MARGIN + BOX_WIDTH * 5 + BOX_SPACING * 4)
            pixel_x = origin[0]
            circles = []
            for i in range(led_count):
                pixel_y = origin[1] - round(led_space * i)
                circles.append(self.draw_circle(pixel_x, pixel_y, size=RAIL_CIRCLE_SIZE))
            self.circles[seg_id] = circles

        # Rows
        for y in range(10):
            for x in range(2):
                seg_id = 2 + x + y * 2
                seg = self.grid.get_seg(seg_id)
                led_count = seg.size()
                seg_length = BOX_WIDTH - (CIRCLE_MARGIN * 2)
                led_space = seg_length / led_count
                origin = coords[x * 2 + y * 4]
                pixel_y = origin[1] - round(CIRCLE_SIZE / 2)
                circles = []
                for i in range(led_count):
                    pixel_x = origin[0] + CIRCLE_MARGIN + round(led_space * i)
                    circles.append(self.draw_circle(pixel_x, pixel_y, size=CIRCLE_SIZE))
                self.circles[seg_id] = circles

        # Columns
        for y in range(5):
            for x in range(4):
                seg_id = 22 + x + y * 4
                seg = self.grid.get_seg(seg_id)
                led_count = seg.size()
                seg_length = BOX_WIDTH - (CIRCLE_MARGIN * 2)
                led_space = seg_length / led_count
                origin = coords[x + y * 8]
                pixel_x = origin[0] - round(CIRCLE_SIZE / 2)
                circles = []
                for i in range(led_count):
                    pixel_y = origin[1] - CIRCLE_MARGIN - round(led_space * i) - CIRCLE_SIZE
                    circles.append(self.draw_circle(pixel_x, pixel_y, size=CIRCLE_SIZE))
                self.circles[seg_id] = circles


    def update(self):
        """
        Update the grid on-screen based on the Grid object.
        """
        for s in range(grid.SEG_COUNT):
            circle_array = self.circles[s]
            color_array = self.grid.get_seg(s).get_pixels()
            for l in range(len(color_array)):
                color = color_array[l]
                r, g, b = color[0], color[1], color[2]
                # TODO: Find source of colors being out of range
                if r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255:
                    print("Error: Color", r, g, b, "out of range.")
                else:
                    hex_color = f'#{r:02x}{g:02x}{b:02x}'
                    self.canvas.itemconfig(circle_array[l], fill=hex_color)


        self.root.update()

    def draw_circle(self, x, y, size):
        """
        :param x: Left x coordinate of circle.
        :param y: Top y coordinate of circle.
        :param size: Circle size.
        :return: The circle ID.
        """

        return self.canvas.create_oval(x, y, x + size, y + size)

    def exit(self):
        """
        Terminate the application.
        """
        sys.exit()
