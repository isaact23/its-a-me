import tkinter as tk
import sys

# Set constants
WIDTH = 100  # Width of each of the squares
MARGIN = 50  # Distance between outside of game and edge of window
DIST = 75  # Distance between railing and tiles
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
        coords.append((MARGIN + DIST + WIDTH * x, MARGIN + WIDTH * y))


# Image generator for the current state of the light show.
class Emulator:
    def __init__(self, grid):
        self.grid = grid

        # Initialize window/canvas
        self.root = tk.Tk()
        self.root.title("Glass Stepping Stones")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.canvas = tk.Canvas(self.root, bg="white", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

        # Horizontal Lines
        for i in range(6):
            self.canvas.create_line(*coords[i * 3], *coords[2 + i * 3], width=LINE_WIDTH)

        # Vertical Lines
        self.canvas.create_line(*TL, *BL, width=LINE_WIDTH)
        self.canvas.create_line(*TR, *BR, width=LINE_WIDTH)
        for i in range(3):
            self.canvas.create_line(*coords[i], *coords[i + 15], width=LINE_WIDTH)

        self.canvas.pack()
        self.root.update()
        self.root.mainloop()

    def update(self):
        """
        Update the grid on-screen.
        """
        self.root.update()

    def exit(self):
        """
        Terminate the application.
        """
        sys.exit()
