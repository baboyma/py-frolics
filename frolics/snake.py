"""
Python Game - SNAKE
SOURCE: https://blog.teclado.com/write-snake-game-python-tkinter-part-1/
"""

import tkinter as tk
from random import randint
from PIL import Image, ImageTk
import copy
from pygame import mixer

MOVE_LEN = 20 # Move by the size of the snake pixels
MPS = 5       # Move Per Second
SPEED = 1000 // MPS

class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

class Snake():
    def __init__(self, app, width, height):
        # Root app/window
        self.app = app

        # App description
        self.name = "Snake Game"
        self.help = "Snake is a genre of action video games where the player maneuvers the end of a growing line, often themed as a snake."

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
        mixer.init()

        # Directions
        self.direction = "Right"
        self.directions = ("Up", "Down", "Left", "Right")
        self.opposites = ({"Up", "Down"}, {"Left", "Right"})

        # Initial Score
        self.score = 0

        # Perform Action
        self.action = ""

        # Snake positions - initial positions should not change after each session
        self.snake_init_positions = [(100, 100), (80, 100), (60, 100)]
        self.snake_positions = copy.deepcopy(self.snake_init_positions)

        # Food positions - Retain initial food position after each sessin
        self.food_init_position = (200, 200)
        self.food_position = copy.deepcopy(self.food_init_position)

        # Initiate Application
        self.initiate()

    def __str__(self):
        return f"{self.name} - {self.help}"

    def intro(self):
        print(self.description)

    def load_assets(self):
        # Default icon/image size
        self.size = 20

        try:
            # Snake head
            self.snake_head_image = Image.open("frolics/assets/images/head.png").resize(size = (self.size, self.size), resample=3)
            self.snake_head = ImageTk.PhotoImage(self.snake_head_image)
            # Snake body
            self.snake_body_image = Image.open("frolics/assets/images/snake.png").resize(size = (self.size, self.size), resample=3)
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
            # Food/Apple
            self.food_image = Image.open("frolics/assets/images/apple.png").resize(size = (self.size, self.size), resample=3)
            self.food = ImageTk.PhotoImage(self.food_image)

            # Sounds
            self.sound_beep = "frolics/assets/sounds/beep.wav"
            self.sound_error = "frolics/assets/sounds/beep-error.wav"
            self.sound_burb = "frolics/assets/sounds/burp-1.wav"

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

        # Toolbar - Movement Direction
        self.movement = tk.Label(self.toolbar,
                                 text = f"MOVE: {self.direction}",
                                 font = (self.fontfamily, self.fontsize),
                                 padx=self.pad, pady=self.pad)

        self.movement.pack(side=tk.LEFT)

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

        # Activate snake motion
        self.action = self.canvas.after(SPEED, self.perform_actions)

    def end_game(self):
        # All re-start at the end of the game
        self.stop.config(state=tk.DISABLED)
        self.start.config(state=tk.NORMAL)

        # Remove game items
        self.canvas.unbind_all("<Key>")
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text = f"GAME OVER!\n\nYou scored {self.score} points!",
            fill = "#FFF",
            font = (self.fontfamily, self.fontsize)
        )

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

        # Play Zone
        self._play_zone = {
            "x0": canvas_grid_gap,
            "y0": canvas_grid_gap,
            "x1": canvas_width - canvas_grid_gap,
            "y1": canvas_height - canvas_grid_gap
        }

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
            self._play_zone["x0"],
            self._play_zone["y0"],
            self._play_zone["x1"],
            self._play_zone["y1"],
            outline="#525d69"
        )

        # Snake
        for x_position, y_position in self.snake_init_positions:
            self.canvas.create_image(
                x_position, y_position, image=self.snake_body, tag="snake"
            )

        # Clear historical positions
        self.snake_positions = copy.deepcopy(self.snake_init_positions)

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

        # New positions - tail is relocated ahead
        self.snake_positions = [head_next_pos] + self.snake_positions[:-1]

        # Update locations of snake's components
        for segment, pos in zip(self.canvas.find_withtag("snake"), self.snake_positions):
            self.canvas.coords(segment, pos)

    def move_food(self):
        # RULE - Avoid replacing the food on top of the snake's head
        while True:
            #pos_x = randint(1, 29) * MOVE_LEN
            pos_x = randint(self._play_zone["x0"], self._play_zone["x1"]//MOVE_LEN) * MOVE_LEN
            #pos_x = randint(self._play_zone["x0"], self._play_zone["x1"])

            #pos_y = randint(3, 30) * MOVE_LEN
            pos_y = randint(self._play_zone["y0"], self._play_zone["y1"]//MOVE_LEN) * MOVE_LEN
            #pos_y = randint(self._play_zone["y0"], self._play_zone["y1"])

            food_pos = (pos_x, pos_y)

            # Exit loop only when food is not on the snake
            if food_pos not in self.snake_positions:
                return food_pos

    def perform_actions(self):
        if self.check_collisions():
            self.play_sound(soundfile=self.sound_error)
            self.end_game()
            return False # Stop there

        if self.check_food_consumption():
            # Update score: +1
            self.update_score(points=1)

            # Relocate food
            self.relocate_food()

            # Update snake length
            self.update_snake()

        # Move snake forward
        self.move_snake()

        self.action = self.canvas.after(SPEED, self.perform_actions)

    def update_score(self, points = 1):
        # Keep track of player's score
        self.score += points
        self.scoreboard.config(text = f"SCORE: {self.score}")

    def update_direction(self, dir = ""):
        # Update movement direction UI
        self.play_sound(soundfile=self.sound_beep)
        self.direction = self.directions[0] if dir == "" else dir
        self.movement.config(text = f"MOVE: {self.direction}")

    def relocate_food(self):
        # Relocate food icon
        self.food_position = self.move_food()
        self.canvas.coords(self.canvas.find_withtag("food"), *self.food_position)

    def update_snake(self):
        # Increase the length of the snake
        self.snake_positions.append(self.snake_positions[-1])
        # Redraw the snake
        self.canvas.create_image(
            *self.snake_positions[-1], image=self.snake_body, tag="snake"
        )

    def check_collisions(self):
        # RULE - Stay within the canvas and do not bite yourself
        head_curr_x, head_curr_y = self.snake_positions[0]

        return(
            #head_curr_x in (7, 583)
            #head_curr_x in (self._play_zone["x0"]-MOVE_LEN, self._play_zone["x1"]+MOVE_LEN)
            head_curr_x not in range(self._play_zone["x0"], self._play_zone["x1"])
            #or head_curr_y in (7, 449)
            #or head_curr_y in (self._play_zone["y0"], self._play_zone["y1"])
            or head_curr_y not in range(self._play_zone["y0"], self._play_zone["y1"])
            or (head_curr_x, head_curr_y) in self.snake_positions[1:]
        )

    def check_food_consumption(self):
        # Check food status
        consumed = False

        # Consumption occurs only when snake head collide with food
        if self.snake_positions[0] == self.food_position:
            consumed = True
            self.play_sound(soundfile=self.sound_burb)

        return consumed

    def on_key_press(self, e):
        # RULE - Snake now allowed to go backward
        new_direction = e.keysym

        if (new_direction in self.directions
            and {new_direction, self.direction} not in self.opposites):
            self.update_direction(new_direction)

    def play_sound(self, soundfile):
        mixer.music.load(soundfile)
        mixer.music.play()

def main():
    app = tk.Tk()

    app.title("SNAKE GAME")
    app.resizable(False, False)
    app.tk.call("tk", "scaling", 4.0)
    app.geometry("500x500")

    apple_eater = Snake(app = app, width=600, height=620)

    print(apple_eater)

    app.mainloop()

if __name__ == "__main__":
    main()
