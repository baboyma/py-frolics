"""
Python Game - SNAKE
SOURCE: https://blog.teclado.com/write-snake-game-python-tkinter-part-1/
"""

import tkinter as tk
from random import randint
from PIL import Image, ImageTk
import copy

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

        # Default GUI Font and Padding
        self.fontfamily = "Verdana"
        self.fontsize = 15
        self.padx = 5
        self.pady = self.padx
        self.pad = self.padx * 2

        # Preset links to key image assets
        self.load_assets()

        # Direction
        self.direction = "Right"

        # Initial Score
        self.score = 0

        # Snake positions
        self.snake_init_positions = [(100, 100), (80, 100), (60, 100)]
        self.snake_positions = copy.deepcopy(self.snake_init_positions)

        # Food positions
        self.food_init_position = (200, 200)
        self.food_position = copy.deepcopy(self.food_init_position)

        # Action - Used to cancel after() when game stops
        self.action = ""

        # Initiate Application
        self.initiate()

    def load_assets(self):
        # Default icon/image size
        self.size = 20

        try:
            # Snake head
            self.snake_head_image = Image.open("./py_frolics/assets/head.png").resize(size = (self.size, self.size), resample=3)
            self.snake_head = ImageTk.PhotoImage(self.snake_head_image)
            # Snake body
            self.snake_body_image = Image.open("./py_frolics/assets/snake.png").resize(size = (self.size, self.size), resample=3)
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
            # Food/Apple
            self.food_image = Image.open("./py_frolics/assets/apple.png").resize(size = (self.size, self.size), resample=3)
            self.food = ImageTk.PhotoImage(self.food_image)

        except IOError as error:
            print(error)
            self.app.destroy()

    def initiate(self):
        # App Header
        self.header = tk.Frame(self.app, padx=self.padx, pady=self.pady)
        self.header.pack(fill = "x")

        self.description = tk.Label(self.header,
                                    text = "SNAKE GAME\nTHE GOAL IS TO GET THE SNAKE TO EAT FOOD\nWITHOUT GETTING OUT OF THE RESTRICTED AREA.",
                                    font = ("Verdana", 15),
                                    pady=self.pad)

        self.description.pack()

        # Add toolbar
        self.toolbar = tk.Frame(self.app, padx=self.padx, pady=self.pady)
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

    def build_gui(self):
        # Toolbar - Start
        self.start = tk.Button(self.toolbar,
                               text="START",
                               cursor = "hand2",
                               padx=self.pad, pady=self.pad,
                               state=tk.NORMAL,
                               command=self.start_game)

        self.start.pack(side=tk.LEFT)

        # Toolbar - Stop
        self.stop = tk.Button(self.toolbar,
                              text="STOP",
                              cursor = "hand2",
                              padx=self.pad, pady=self.pad,
                              state=tk.DISABLED,
                              command=self.end_game)

        self.stop.pack(side=tk.LEFT)

        # Toolbar - Score board
        self.scoreboard = tk.Label(self.toolbar,
                                   text = f"SCORE: {self.score}",
                                   font = (self.fontfamily, self.fontsize),
                                   padx=self.pad, pady=self.pad)

        self.scoreboard.pack(side=tk.LEFT)

        # Add Game Canvas & bind key press events
        self.create_objects()
        self.canvas.bind_all("<Key>", self.on_key_press)

        # Hide Show Tool
        self.show.config(state=tk.DISABLED)

    def start_game(self):
        # Disable Start Tool
        self.start.config(state=tk.DISABLED)
        self.stop.config(state=tk.NORMAL)

        # Check re-start
        if "snake" not in self.canvas.image_names():
            self.create_objects()
            self.canvas.bind_all("<Key>", self.on_key_press)

        # Active Snake motion
        self.action = self.canvas.after(SPEED, self.perform_actions)

    def end_game(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text = f"GAME OVER!\n\nYou scored {self.score} points!",
            fill = "#FFF",
            font = (self.fontfamily, self.fontsize)
        )

        # All re-start at the end of the game
        self.stop.config(state=tk.DISABLED)
        self.start.config(state=tk.NORMAL)

        # Cancel action
        self.canvas.after_cancel(self.action)

    def restart_game(self):
        self.canvas.destroy()
        self.create_objects()
        self.start_game()

    def create_objects(self):
        # Create new Canvas
        # Dimensions and top Gap
        canvas_tgap = self.header.winfo_height() + self.toolbar.winfo_height() + (self.pad * 2)
        canvas_width = self.width - self.pad
        canvas_height = self.height - canvas_tgap
        canvas_grid_gap = 7

        # Canvas
        if hasattr(self, "canvas") is False:
            self.canvas = tk.Canvas(self.app,
                                    width = canvas_width,
                                    height = canvas_height,
                                    background="black",
                                    highlightthickness=0)

            self.canvas.pack()
        else:
            self.canvas.delete(tk.ALL)

        # Play area - rectangle
        self.canvas.create_rectangle(
            canvas_grid_gap,
            canvas_grid_gap,
            canvas_width - 7,
            canvas_height - 7,
            outline="#525d69"
        )

        # Snake
        for x_position, y_position in self.snake_init_positions:
            self.canvas.create_image(
                x_position, y_position, image=self.snake_body, tag="snake"
            )

        # Food
        self.canvas.create_image(*self.food_init_position, image=self.food, tag="food")

        # Reset Score
        self.score = 0
        self.update_score(points = 0)

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
        # RULE - Avoid replacing the food on top of the snake's head
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

    def update_score(self, points = 1):
        # Keep track of player's score
        self.score += points
        self.scoreboard.config(text = f"SCORE: {self.score}")

    def check_collisions(self):
        # RULE - Stay within the canvas and do not bite yourself
        head_curr_x, head_curr_y = self.snake_positions[0]

        return(
            head_curr_x in (0, self.width)
            or head_curr_y in (20, self.height)
            or (head_curr_x, head_curr_y) in self.snake_positions[1:]
        )

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.update_score()

            self.snake_positions.append(self.snake_positions[-1])

            self.canvas.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )

            self.food_position = self.move_food()
            self.canvas.coords(self.canvas.find_withtag("food"), *self.food_position)

            #score = self.canvas.find_withtag("score")
            #self.canvas.itemconfigure(score, text = f"Score: {self.score}", tag="score")
            #self.scoreboard.config(text = f"SCORE: {self.score}")

    def on_key_press(self, e):
        # RULE - Snake now allowed to go backward
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
