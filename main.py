"""By Matthew Leith"""
import tkinter as tk
HEIGHT = 400
WIDTH = 200


class Level:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root,
                                height=self.root.winfo_height(),
                                width=self.root.winfo_width(),
                                bg="green")
        self.canvas.pack()


class TitleScreen:
    def __init__(self, root):
        self.root = root
        self.title_frame = tk.Frame(self.root)
        self.title_label = tk.Label(self.title_frame, text="Welcome to Flappy Bird")
        self.title_label.pack()
        self.play_button = tk.Button(self.title_frame, text="Play", command=self.play)
        self.play_button.pack()
        self.title_frame.pack()
        self.level = None

    def play(self):
        self.title_frame.pack_forget()
        self.level = Level(self.root)


class Game:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Flappy Bird - Matt Leith Edition")
        self.root.geometry("400x400")
        self.title_screen = TitleScreen(self.root)
        self.root.mainloop()


new_game = Game()


