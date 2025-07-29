"""
Game Idea: "Color Catchers"

Concept:

A simple game where toddlers can learn to associate colors with shapes.
The game features a colorful background and animated falling shapes (circles, squares, triangles).
Toddlers use the mouse to "catch" the falling shapes in corresponding colored bins.
"""

import tkinter as tk
from random import randint, choice
from PIL import Image, ImageTk
import copy
from pygame import mixer

# ... (Shape creation, movement, etc.)

class Catcher(tk.Tk):
    """ COLOR CATCHER """
    def __init__(self, name, width, height):
        super().__init__()

        # App description
        self.title(name.upper())
        self.help = "Color Catcher is a game where the play sse the mouse to catch the falling shapes in corresponding colored bins"

        # Dimensions
        self.width = width
        self.height = height
        self.geometry(f"{width}x{height}")

        # Default GUI Font and Padding
        self.fontfamily = "Verdana"
        self.fontsize = 15
        self.padx = 5
        self.pady = self.padx
        self.pad = self.padx * 2

        # Preset links to key image assets
        #self.load_assets()
        mixer.init()

        # Directions
        self.direction = "Right"
        self.directions = ("Left", "Right")
        self.opposites = ({"Up", "Down"}, {"Left", "Right"})

        # Initial Score
        self.score = 0

        # Perform Action
        self.action = ""

        # Target Shapes
        self.shapes = [{"square": "red"}, {"triangle": "green"}, {"circle": "blue"}]
        #self.shape = choice(set().union(*[shp.keys() for shp in self.shapes]))
        #self.color = choice([shp.values() for shp in self.shapes])

        # Snake positions - initial positions should not change after each session
        self.shapes_init_positions = [(100, 100), (80, 100), (60, 100)]
        self.shapes_positions = copy.deepcopy(self.shapes_init_positions)

        # Food positions - Retain initial food position after each sessin
        self.catcher_init_position = (200, 200)
        self.catcher_position = copy.deepcopy(self.catcher_init_position)

        # Initiate Application
        self.initiate()

    def initiate(self):
        # App Header
        self.header = tk.Frame(self, padx=self.padx, pady=self.pady)
        self.header.pack(fill = "x")

        self.description = tk.Label(self.header,
                                    text = self.help.upper(),
                                    wraplength=round(self.width * 3/4),
                                    font = ("Verdana", 15),
                                    pady=self.pad)

        self.description.pack()

        # Add toolbar
        self.toolbar = tk.Frame(self, padx=self.padx, pady=self.pady)
        self.toolbar.pack(fill = "x")

        # Toolbar - Show
        self.show = tk.Button(self.toolbar,
                              text="SHOW GAME",
                              cursor="hand2",
                              padx=self.pad, pady=self.pad, bd = 2,
                              state=tk.NORMAL,
                              command=self.build_gui)

        self.show.pack(side=tk.LEFT)
        self.show.lift()

        # Dimensions and top Gap
        canvas_tgap = self.header.winfo_height() + self.toolbar.winfo_height() + (self.pad * 2)
        canvas_width = self.width - self.pad
        canvas_height = self.height - canvas_tgap
        canvas_grid_gap = 7

        # Play Zone
        self._play_zone = {
            "x0": canvas_grid_gap,
            "y0": canvas_grid_gap,
            "x1": canvas_width - canvas_grid_gap,
            "y1": canvas_height - canvas_grid_gap
        }

        # Canvas
        self.canvas = tk.Canvas(self,
                                width = canvas_width,
                                height = canvas_height,
                                background="black",
                                highlightthickness=0)

        self.canvas.pack()

        # Play area - rectangle
        self.canvas.create_rectangle(
            self._play_zone["x0"],
            self._play_zone["y0"],
            self._play_zone["x1"],
            self._play_zone["y1"],
            outline="#525d69"
        )

        # Draw the catcher line at the bottom of the canvas
        self.draw_catcher()

        # Draw shapes at initial positions
        self.draw_shapes()

    def build_gui(self):
        pass

    def draw_catcher(self):
        self.canvas.create_line(
            self._play_zone['x0'] + (self.pad * 2),
            self._play_zone['y1'] - (self.pad * 5),
            self._play_zone['x1'] - (self.pad * 2),
            self._play_zone['y1'] - (self.pad * 5),
            width = 20,
            fill = "#FFF"
        )

    def draw_(self):
        self.canvas.create_line(
            self._play_zone['x0'] + (self.pad * 2),
            self._play_zone['y1'] - (self.pad * 5),
            self._play_zone['x1'] - (self.pad * 2),
            self._play_zone['y1'] - (self.pad * 5),
            width = 20,
            fill = "#FFF"
        )

    def draw_shapes(self):
        r = 100
        shp_y = self._play_zone['y0'] + r + (r/2)
        shp_x = (self._play_zone['x0'] - self._play_zone['x0']) / len(self.shapes)

        self.canvas.create_oval(
            self._play_zone['x0'] + (self.pad * 3),
            self._play_zone['y0'] + (self.pad * 3),
            self._play_zone['x0'] + (self.pad * 10),
            self._play_zone['y0'] + (self.pad * 10),
            width = 2,
            fill = "#FFF"
        )

def check_bin_catch(x, y):
    red_bin_x1, red_bin_x2, red_bin_y1, red_bin_y2 = 100
    # ... (Check if click coordinates are within a bin)
    if x in range(red_bin_x1, red_bin_x2) and y in range(red_bin_y1, red_bin_y2):
        # ... (Handle red bin catch)
        pass
    elif y in range(1, 299):
        # ... (Handle other bin catches)
        pass


def main():
    #root.bind("<Button-1>", lambda event: check_bin_catch(event.x, event.y))
    #root.mainloop()
    catcher = Catcher(name = "Color Catcher", width=700, height=600)
    catcher.mainloop()