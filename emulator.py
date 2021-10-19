import tkinter as tk
import sys
from time import perf_counter

# Set constants
WIDTH = 100  # Width of each of the squares
MARGIN = 50  # Distance between outside of game and edge of window
DIST = 75  # Distance between railing and tiles
CIRCLE_MARGIN = 0  # Distance between coordinates and first circle of each Segment
CIRCLE_SIZE = 5
RAIL_CIRCLE_SIZE = 10
LINE_WIDTH = 2

# Determine window size
WINDOW_WIDTH = MARGIN * 2 + DIST * 2 + WIDTH * 2
WINDOW_HEIGHT = MARGIN * 2 + WIDTH * 5

# Generate railing coordinates
TL = (MARGIN, MARGIN)
BL = (MARGIN, MARGIN + WIDTH * 5)
TR = (MARGIN + DIST * 2 + WIDTH * 2, MARGIN)
BR = (MARGIN + DIST * 2 + WIDTH * 2, MARGIN + WIDTH * 5)
# Generate grid coordinates
coords = []
for y in range(6):
    for x in range(3):
        coords.append((MARGIN + DIST + WIDTH * x, MARGIN + WIDTH * (5 - y)))


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
                seg_length = WIDTH - (CIRCLE_MARGIN * 2)
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
                seg_length = WIDTH - (CIRCLE_MARGIN * 2)
                led_space = seg_length / led_count
                origin = coords[x + y * 3]
                pixel_y = origin[1] - round(CIRCLE_SIZE / 2)
                circles = []
                for i in range(led_count):
                    pixel_x = origin[0] + CIRCLE_MARGIN + round(led_space * i)
                    circles.append(self.draw_circle(pixel_x, pixel_y, size=CIRCLE_SIZE))
                self.circles[seg_id] = circles

        # Railings
        seg_length = (WIDTH * 5) - (CIRCLE_MARGIN * 2)
        for x in range(2):
            seg_id = 27 + x
            seg = self.grid.get_seg(seg_id)
            led_count = seg.size()
            led_space = seg_length / led_count
            if x == 0:
                origin = (MARGIN, MARGIN + WIDTH * 5)
            else:
                origin = (MARGIN + DIST * 2 + WIDTH * 2, MARGIN + WIDTH * 5)
            pixel_x = origin[0]
            circles = []
            for i in range(led_count):
                pixel_y = origin[1] - round(led_space * i)
                circles.append(self.draw_circle(pixel_x, pixel_y, size=RAIL_CIRCLE_SIZE))
            self.circles[seg_id] = circles

    def update(self):
        """
        Update the grid on-screen based on the Grid object.
        """
        for s in range(29):
            circle_array = self.circles[s]
            color_array = self.grid.get_seg(s).get_pixels()
            for l in range(len(color_array)):
                color = color_array[l]
                r, g, b = color[0], color[1], color[2]
                try:
                    hex_color = f'#{r:02x}{g:02x}{b:02x}'
                except ValueError:
                    raise RuntimeError("LED strip updated with float color value", r, g, b)
                self.canvas.itemconfig(circle_array[l], fill=hex_color)

        self.root.update()

    def draw_circle(self, x, y, size):
        """
        :param x: Left x coordinate of circle.
        :param y: Top y coordinate of circle.
        :param color: RGB circle color.
        :return: The circle ID.
        """
        # Convert RGB color to tkinter format
        # r, g, b = color[0], color[1], color[2]
        # hex_color = f'#{r:02x}{g:02x}{b:02x}'

        return self.canvas.create_oval(x, y, x + size, y + size)

    def exit(self):
        """
        Terminate the application.
        """
        sys.exit()
