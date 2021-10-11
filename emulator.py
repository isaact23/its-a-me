import tkinter as tk
import sys

# Set constants
WIDTH = 100  # Width of each of the squares
MARGIN = 50  # Distance between outside of game and edge of window
DIST = 75  # Distance between railing and tiles
CIRCLE_MARGIN = 10  # Distance between coordinates and first circle of each Segment
CIRCLE_SIZE = 5
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

        self.update()
        self.root.mainloop()

    def update(self):
        """
        Update the grid on-screen based on the Grid.
        """
        # Columns
        for y in range(5):
            for x in range(3):
                seg = self.grid.get_segment(12 + x + y * 3)
                led_count = seg.size()
                seg_length = WIDTH - (CIRCLE_MARGIN * 2)
                led_space = seg_length / led_count
                pixels = seg.get_pixels()
                origin = coords[x + y * 3]
                pixel_x = origin[0] - round(CIRCLE_SIZE / 2)
                for i in range(led_count):
                    pixel_y = origin[1] - CIRCLE_MARGIN - round(led_space * i) - CIRCLE_SIZE
                    self.draw_circle(pixel_x, pixel_y, pixels[i])
        # Rows
        for y in range(6):
            for x in range(2):
                seg = self.grid.get_segment(x + y * 2)
                led_count = seg.size()
                seg_length = WIDTH - (CIRCLE_MARGIN * 2)
                led_space = seg_length / led_count
                pixels = seg.get_pixels()
                origin = coords[x + y * 3]
                pixel_y = origin[1] - round(CIRCLE_SIZE / 2)
                for i in range(led_count):
                    pixel_x = origin[0] + CIRCLE_MARGIN + round(led_space * i)
                    self.draw_circle(pixel_x, pixel_y, pixels[i])

        # Railings
        seg_length = (WIDTH * 5) - (CIRCLE_MARGIN * 2)
        for x in range(2):
            seg = self.grid.get_segment(27 + x)
            led_count = seg.size()
            led_space = seg_length / led_count
            pixels = seg.get_pixels()
            if x == 0:
                origin = (MARGIN, MARGIN + WIDTH * 5)
            else:
                origin = (MARGIN + DIST * 2 + WIDTH * 2, MARGIN + WIDTH * 5)
            pixel_x = origin[0]
            for i in range(led_count):
                pixel_y = origin[1] - round(led_space * i) - CIRCLE_MARGIN - CIRCLE_SIZE
                self.draw_circle(pixel_x, pixel_y, pixels[i])

        self.root.update()

    def draw_circle(self, x, y, color):
        """
        :param x: Left x coordinate of circle.
        :param y: Top y coordinate of circle.
        :param color: RGB circle color.
        """
        # Convert RGB color to tkinter format
        r, g, b = color[0], color[1], color[2]
        hex_color = f'#{r:02x}{g:02x}{b:02x}'

        self.canvas.create_oval(x, y, x + CIRCLE_SIZE, y + CIRCLE_SIZE, fill=hex_color)#, outline="")

    def exit(self):
        """
        Terminate the application.
        """
        sys.exit()
