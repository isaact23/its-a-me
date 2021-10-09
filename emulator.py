import tkinter as tk
import sys

WIDTH = 100  # Width of each of the squares
MARGIN = 50  # Distance between outside of game and edge of window
DIST = 75  # Distance between railing and tiles
LINE_WIDTH = 1


# Image generator for the current state of the light show.
class Emulator:
    def __init__(self, grid):
        self.grid = grid

        # Initialize window/canvas
        self.root = tk.Tk()
        self.root.title("Glass Stepping Stones")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.canvas = tk.Canvas(self.root, bg="white", width=(MARGIN * 2 + DIST * 2 + WIDTH * 2),
                                height=(MARGIN * 2 + WIDTH * 5))
        # Horizontal Lines
        self.canvas.create_line(MARGIN + DIST, MARGIN, MARGIN + DIST + WIDTH * 2, MARGIN, width=LINE_WIDTH)
        self.canvas.create_line(MARGIN + DIST, MARGIN + WIDTH, MARGIN + DIST + WIDTH * 2, MARGIN + WIDTH,
                                width=LINE_WIDTH)
        self.canvas.create_line(MARGIN + DIST, MARGIN + WIDTH * 2, MARGIN + DIST + WIDTH * 2, MARGIN + WIDTH * 2,
                                width=LINE_WIDTH)
        self.canvas.create_line(MARGIN + DIST, MARGIN + WIDTH * 3, MARGIN + DIST + WIDTH * 2, MARGIN + WIDTH * 3,
                                width=LINE_WIDTH)
        self.canvas.create_line(MARGIN + DIST, MARGIN + WIDTH * 4, MARGIN + DIST + WIDTH * 2, MARGIN + WIDTH * 4,
                                width=LINE_WIDTH)
        self.canvas.create_line(MARGIN + DIST, MARGIN + WIDTH * 5, MARGIN + DIST + WIDTH * 2, MARGIN + WIDTH * 5,
                                width=LINE_WIDTH)
        # Vertical Lines
        self.canvas.create_line(MARGIN, MARGIN, MARGIN, MARGIN + WIDTH * 5, width=LINE_WIDTH)
        self.canvas.create_line(MARGIN + DIST, MARGIN, MARGIN + DIST, MARGIN + WIDTH * 5, width=LINE_WIDTH)
        self.canvas.create_line(MARGIN + DIST + WIDTH, MARGIN, MARGIN + DIST + WIDTH, MARGIN + WIDTH * 5,
                                width=LINE_WIDTH)
        self.canvas.create_line(MARGIN + DIST + WIDTH * 2, MARGIN, MARGIN + DIST + WIDTH * 2, MARGIN + WIDTH * 5,
                                width=LINE_WIDTH)
        self.canvas.create_line(MARGIN + DIST * 2 + WIDTH * 2, MARGIN, MARGIN + DIST * 2 + WIDTH * 2,
                                MARGIN + WIDTH * 5, width=LINE_WIDTH)
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
