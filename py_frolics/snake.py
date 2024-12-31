"""
Python Game - SNAKE
SOURCE: https://blog.teclado.com/write-snake-game-python-tkinter-part-1/
"""

import tkinter as tk
from random import randint
from PIL import Image, ImageTk

MOVE_LEN = 20
MPS = 5
SPEED = 1000 // MPS

class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, width=500, height=500)
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
        self.button1.pack()
        self.frame.pack()
    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
    def close_windows(self):
        self.master.destroy()

class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

class Snake():
    def __init__(self, app, width, height):
        # Root app/window
        self.app = app

        # Dimensions
        self.width = width
        self.height = height
        self.app.geometry(f"{width}x{height}")

        # Preset links to key image assets
        self.load_assets()

        # Direction
        self.direction = "Right"

        # Initial Score
        self.score = 0

        # Initial position of snake & food
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = (200, 200)

        # Initiate Application
        self.initiate()

    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./py_frolics/assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("./py_frolics/assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)

        except IOError as error:
            print(error)
            root.destroy()

    def initiate(self):
        # App Header
        self.header = tk.Frame(app, padx=5, pady=5)
        self.header.pack(fill = "x")

        self.description = tk.Label(self.header,
                                    text = "SNAKE GAME\nTHE GOAL IS TO GET THE SNAKE TO EAT FOOD\nWITHOUT GETTING OUT OF THE RESTRICTED AREA.",
                                    font = ("Verdana", 15),
                                    pady=10)

        self.description.pack()

        # Add toolbar
        self.toolbar = tk.Frame(app, padx=5, pady=5)
        self.toolbar.pack(fill = "x")

        # Toolbar - Show
        self.show = tk.Button(self.toolbar,
                              text="SHOW GAME",
                              cursor="hand2",
                              padx=10, pady=10, bd = 2,
                              command=self.build_game)

        self.show.pack(side=tk.LEFT)
        #self.show.lift()

    def build_game(self):
        # Toolbar - Start
        self.start = tk.Button(self.toolbar,
                               text="START",
                               cursor = "hand2",
                               padx=10, pady=10,
                               command=self.start_game)

        self.start.pack(side=tk.LEFT)

        # Toolbar - Stop
        self.stop = tk.Button(self.toolbar,
                              text="STOP",
                              cursor = "hand2",
                              padx=10, pady=10,
                              state=tk.NORMAL,
                              command=self.end_game)

        self.stop.pack(side=tk.LEFT)

        # Add Game Canvas & bind key press events
        self.create_objects()
        self.canvas.bind_all("<Key>", self.on_key_press)

        # Hide Show Tool
        self.show.config(state=tk.DISABLED)

    def start_game(self):
        # Disable Start Tool
        self.start.config(state=tk.DISABLED)
        self.stop.config(state=tk.NORMAL)

        # Active Snake motion
        self.canvas.after(SPEED, self.perform_actions)

    def end_game(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text = f"GAME OVER! You scored {self.score}!",
            fill = "#FFF",
            font = ("", 15)
        )

        # All re-start at the end of the game
        self.stop.config(state=tk.DISABLED)
        self.start.config(state=tk.NORMAL)

    def restart_game(self):
        self.canvas.destroy()
        self.create_objects()
        self.start_game()

    def create_objects(self):
        # Create New Canvas
        self.canvas = tk.Canvas(self.app,
                                width=self.width - 20,
                                height=self.height - 100,
                                background="black",
                                highlightthickness=0)

        # Scoring box - Text
        self.canvas.create_text(
            35, 12,
            text = f"Score: {self.score}",
            tag = "score", fill="#FFF", font=15
        )

        # Snake
        for x_position, y_position in self.snake_positions:
            self.canvas.create_image(
                x_position, y_position, image=self.snake_body, tag="snake"
            )

        # Food
        self.canvas.create_image(*self.food_position, image=self.food, tag="food")

        # Play area - rectangle
        self.canvas.create_rectangle(7, 27, 586, 613, outline="#525d69")

        self.canvas.pack()

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
        elif self.direction == "Up":
            head_next_pos = (head_curr_x, head_curr_y - MOVE_LEN)

        # New position
        self.snake_positions = [head_next_pos] + self.snake_positions[:-1]

        for segment, pos in zip(self.canvas.find_withtag("snake"), self.snake_positions):
            self.canvas.coords(segment, pos)

    def move_food(self):
        while True:
            pos_x = randint(1, 29) * MOVE_LEN
            pos_y = randint(3, 30) * MOVE_LEN

            food_pos = (pos_x, pos_y)

            if food_pos not in self.snake_positions:
                return food_pos

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()

        self.check_food_collision()
        self.move_snake()

        self.canvas.after(SPEED, self.perform_actions)

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

            self.canvas.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )

            self.food_position = self.move_food()
            self.canvas.coords(self.canvas.find_withtag("food"), *self.food_position)

            score = self.canvas.find_withtag("score")
            self.canvas.itemconfigure(score, text = f"Score: {self.score}", tag="scrore")

    def on_key_press(self, e):
        new_direction = e.keysym

        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (new_direction in all_directions
            and {new_direction, self.direction} not in opposites):
            self.direction = new_direction

app = tk.Tk()
app.title("SNAKE GAME")
app.resizable(False, False)
app.tk.call("tk", "scaling", 4.0)
app.geometry("500x500")

board = Snake(app, width=600, height=620)

app.mainloop()
