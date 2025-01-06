import tkinter as tk
from frolics.snake import Snake

app = tk.Tk()
app.title("SNAKE GAME")
app.resizable(False, False)
app.tk.call("tk", "scaling", 4.0)
app.geometry("500x500")

board = Snake(app, width=600, height=620)

app.mainloop()