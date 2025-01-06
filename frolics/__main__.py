import tkinter as tk
import argparse
from frolics.snake import Snake, main as snake_start

def snake_startttt():
    """ Start Snake Game from command line"""
    app = tk.Tk()
    app.title("SNAKE GAME")
    app.resizable(False, False)
    app.tk.call("tk", "scaling", 4.0)
    app.geometry("500x500")

    snake = Snake(app = app, width=600, height=620)

    print(snake)

    app.mainloop()

# Parse module argements

parser = argparse.ArgumentParser(description="Python games")
parser.add_argument("-g", "--game", required=True, choices=["snake", "catcher"], help="Name of the game")

args = parser.parse_args()

# Start requested case:
match args.game.lower():
    case "snake":
        print("Starting SNAKE game ...")
        snake_start()
    case "catcher":
        print("COLOR CATCHER is under development. Check back later ...")
    case _:
        print("NO GAME specified - Running SNAKE instead ...")
        snake_start()