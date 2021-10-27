import math
import tkinter as tk
import sys
from time import perf_counter

# Set constants
import grid

BOX_WIDTH = 100  # Width of each of the squares
MARGIN = 75  # Distance between outside of game and edge of window
RAILING_DIST = 75  # Distance between railing and tiles
BOX_SPACING = 25  # Distance between squares
CIRCLE_MARGIN = 0  # Distance between coordinates and first circle of each Segment
PUMPKIN_RADIUS = 20
PUMPKIN_DISTANCE = 70  # Distance between pumpkins and bottom of grid

LINE_WIDTH = 2
CIRCLE_SIZE = 7
RAIL_CIRCLE_SIZE = 9
PUMPKIN_CIRCLE_SIZE = 8

# Determine window size
WINDOW_WIDTH = MARGIN * 2 + RAILING_DIST * 2 + BOX_WIDTH * 2 + BOX_SPACING
WINDOW_HEIGHT = MARGIN * 2 + BOX_WIDTH * 5 + PUMPKIN_DISTANCE + BOX_SPACING * 4

# Generate railing coordinates
TL = (MARGIN, MARGIN)
BL = (MARGIN, MARGIN + BOX_WIDTH * 5)
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

        # Horizontal Lines
        for i in range(6):
            self.canvas.create_line(*coords[i * 3], *coords[2 + i * 3], width=LINE_WIDTH)

        # Vertical Lines
        self.canvas.create_line(*TL, *BL, width=LINE_WIDTH)
        self.canvas.create_line(*TR, *BR, width=LINE_WIDTH)
        for i in range(3):
            self.canvas.create_line(*coords[i], *coords[i + 15], width=LINE_WIDTH)

        self.canvas.pack()
        self.gen_circles()
        self.update()

    def gen_circles(self):
        """
        Create all circle objects representative of individual LEDs.
        """
        # Columns
        for y in range(5):
            for x in range(3):
                seg_id = 12 + x + y * 3
                seg = self.grid.get_seg(seg_id)
                led_count = seg.size()
                seg_length = BOX_WIDTH - (CIRCLE_MARGIN * 2)
                led_space = seg_length / led_count
                origin = coords[x + y * 3]
                pixel_x = origin[0] - round(CIRCLE_SIZE / 2)
                circles = []
                for i in range(led_count):
                    pixel_y = origin[1] - CIRCLE_MARGIN - round(led_space * i) - CIRCLE_SIZE
                    circles.append(self.draw_circle(pixel_x, pixel_y, size=CIRCLE_SIZE))
                self.circles[seg_id] = circles

        # Rows
        for y in range(6):
            for x in range(2):
                seg_id = x + y * 2
                seg = self.grid.get_seg(seg_id)
                led_count = seg.size()
                seg_length = BOX_WIDTH - (CIRCLE_MARGIN * 2)
                led_space = seg_length / led_count
                origin = coords[x + y * 3]
                pixel_y = origin[1] - round(CIRCLE_SIZE / 2)
                circles = []
                for i in range(led_count):
                    pixel_x = origin[0] + CIRCLE_MARGIN + round(led_space * i)
                    circles.append(self.draw_circle(pixel_x, pixel_y, size=CIRCLE_SIZE))
                self.circles[seg_id] = circles

        # Railings
        seg_length = (BOX_WIDTH * 5) - (CIRCLE_MARGIN * 2)
        for x in range(2):
            seg_id = 27 + x
            seg = self.grid.get_seg(seg_id)
            led_count = seg.size()
            led_space = seg_length / led_count
            if x == 0:
                origin = (MARGIN, MARGIN + BOX_WIDTH * 5)
            else:
                origin = (MARGIN + RAILING_DIST * 2 + BOX_WIDTH * 2, MARGIN + BOX_WIDTH * 5)
            pixel_x = origin[0]
            circles = []
            for i in range(led_count):
                pixel_y = origin[1] - round(led_space * i)
                circles.append(self.draw_circle(pixel_x, pixel_y, size=RAIL_CIRCLE_SIZE))
            self.circles[seg_id] = circles

        # Pumpkins
        def gen_pumpkin_coords(center, radius, count):
            coords = []
            for i in range(count):
                coords.append((
                    center[0] + radius * math.sin(i * 2 * math.pi / count),
                    center[1] + radius * math.cos(i * 2 * math.pi / count)
                ))
            return coords

        left_center = (MARGIN, MARGIN + BOX_WIDTH * 5 + PUMPKIN_DISTANCE)
        left_seg = self.grid.get_seg(29)
        left_coords = gen_pumpkin_coords(left_center, PUMPKIN_RADIUS, left_seg.size())
        left_circles = []
        for coord in left_coords:
            left_circles.append(self.draw_circle(*coord, size=PUMPKIN_CIRCLE_SIZE))
        self.circles[29] = left_circles

        right_center = (MARGIN + RAILING_DIST * 2 + BOX_WIDTH * 2, MARGIN + BOX_WIDTH * 5 + PUMPKIN_DISTANCE)
        right_seg = self.grid.get_seg(30)
        right_coords = gen_pumpkin_coords(right_center, PUMPKIN_RADIUS, right_seg.size())
        right_circles = []
        for coord in right_coords:
            right_circles.append(self.draw_circle(*coord, size=PUMPKIN_CIRCLE_SIZE))
        self.circles[30] = right_circles


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
                try:
                    hex_color = f'#{r:02x}{g:02x}{b:02x}'
                    self.canvas.itemconfig(circle_array[l], fill=hex_color)
                except:
                    raise RuntimeError("Attempted LED strip update with float color value", r, g, b)


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
