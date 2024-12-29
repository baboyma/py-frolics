"""
Python Game - SNAKE
SOURCE: https://blog.teclado.com/write-snake-game-python-tkinter-part-1/
"""

import tkinter as tk
from random import randint
from PIL import Image, ImageTk

MOVE_LEN = 20
MPS = 15
SPEED = 1000 // MPS

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(
            width=600,
            height=620,
            background="black",
            highlightthickness=0
        )

        # Direction
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)

        # Initial Score
        self.score = 0

        # Initial position of snake & food
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = (200, 200)

        # Preset links to key image assets
        self.load_assets()

        # Create images
        self.create_objects()

        self.after(SPEED, self.perform_actions)

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
        # Scoring box - Text
        self.create_text(
            35, 12,
            text = f"Score: {self.score}",
            tag = "score", fill="#FFF", font=15
        )
        # Snake
        for x_position, y_position in self.snake_positions:
            self.create_image(
                x_position, y_position, image=self.snake_body, tag="snake"
            )
        # Food
        self.create_image(*self.food_position, image=self.food, tag="food")
        # Play area - rectangle
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")

    def move_snake(self):
        # Identify the position of the head of the snake
        head_curr_x, head_curr_y = self.snake_positions[0]
        #head_next_pos = (head_curr_x + MOVE_LEN, head_curr_y)

        if self.direction == "Left":
            head_next_pos = (head_curr_x - MOVE_LEN, head_curr_y)
        elif self.direction == "Right":
            head_next_pos = (head_curr_x + MOVE_LEN, head_curr_y)
        elif self.direction == "Down":
            head_next_pos = (head_curr_x, head_curr_y + MOVE_LEN)
        elif self.direction == "Top":
            head_next_pos = (head_curr_x, head_curr_y - MOVE_LEN)

        # New position
        self.snake_positions = [head_next_pos] + self.snake_positions[:-1]

        for segment, pos in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, pos)

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()

        self.check_food_collision()
        self.move_snake()

        self.after(SPEED, self.perform_actions)

    def check_collisions(self):
        head_curr_x, head_curr_y = self.snake_positions[0]

        return(
            head_curr_x in (0, 600)
            or head_curr_y in (20, 620)
            or (head_curr_x, head_curr_y) in self.snake_positions[1:]
        )

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )

            self.food_position = self.move_food()
            self.coords(self.find_withtag("food"), *self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text = f"Score: {self.score}", tag="scrore")

    def move_food(self):
        while True:
            pos_x = randint(1, 29) * MOVE_LEN
            pos_y = randint(3, 30) * MOVE_LEN

            food_pos = (pos_x, pos_y)

            if food_pos not in self.snake_positions:
                return food_pos

    def on_key_press(self, e):
        new_direction = e.keysym

        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (new_direction in all_directions
            and {new_direction, self.direction} not in opposites):
            self.direction = new_direction

    def start_game(self):
        # Create images
        self.create_objects()
        self.after(SPEED, self.perform_actions)

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text = f"GAME OVER! You scored {self.score}!",
            fill = "#FFF",
            font = ("", 15)
        )


root = tk.Tk()
root.title("SNAKE GAME")
root.resizable(False, False)
root.tk.call("tk", "scaling", 4.0)

board = Snake()

root.mainloop()