"""By Matthew Leith"""
import tkinter as tk
HEIGHT = 400
WIDTH = 200
BIRD_SIZE = 30
x1 = 20
y1 = 50
MAX_FALL_SPEED = 10


class Bird:
    def __init__(self, level):
        self.level = level
        self.box = level.canvas.create_rectangle(x1, x1 + BIRD_SIZE,
                                                 y1, y1 - BIRD_SIZE,
                                                 fill="gold1")
        self.falling_speed = 0
        self.weight()

    def jump(self, foo):
        self.falling_speed = -3

    def weight(self):
        """Supposed to be the weight force"""
        if self.falling_speed < MAX_FALL_SPEED:
            self.falling_speed += 0.1
        # Update position
        self.level.canvas.move(self.box, 0, self.falling_speed)
        self.level.canvas.after(10, self.weight)


class Level:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root,
                                height=self.root.winfo_height(),
                                width=self.root.winfo_width(),
                                bg="green")
        self.canvas.pack()
        self.bird = Bird(self)
        self.root.bind('<space>', self.bird.jump)


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


