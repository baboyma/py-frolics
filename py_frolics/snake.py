"""
Python Game - SNAKE
SOURCE: https://blog.teclado.com/write-snake-game-python-tkinter-part-1/
"""

import tkinter as tk
from PIL import Image, ImageTk

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(
            width=600,
            height=620,
            background="black",
            highlightthickness=0
        )

        # Initial position of snake & food
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = (200, 200)

        # Preset links to key image assets
        self.load_assets()

        # Create images
        self.create_objects()

        self.pack()

    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./py_frolics/assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("./py_frolics/assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)

        except IOError as error:
            print(error)
            root.destroy()

    def create_objects(self):
        # Snake
        for x_position, y_position in self.snake_positions:
            self.create_image(
                x_position, y_position, image=self.snake_body, tag="snake"
            )
        # Food
        self.create_image(*self.food_position, image=self.food, tag="food")

root = tk.Tk()
root.title("SNAKE GAME")
root.resizable(False, False)
root.tk.call("tk", "scaling", 4.0)

board = Snake()

root.mainloop()