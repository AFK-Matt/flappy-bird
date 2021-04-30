"""By Matthew Leith"""
import tkinter as tk
HEIGHT = 400
WIDTH = 200
BIRD_SIZE = 20  # Width and height of the square bird
x1 = 30  # Pixels between the right edge of bird and left edge of canvas
y1 = WIDTH/2  # Pixels from the top of the screen the bottom of the bird spawns
MAX_FALL_SPEED = 10
MS_BETWEEN_TICKS = 10  # Milliseconds between each tick
GROUND_HEIGHT = 23  # Pixels that the ground is above the bottom of canvas


class Bird:
    """Handle the movements and graphics of the bird."""

    def __init__(self, level):
        """Create the bird, initialise falling_speed."""
        self.level = level
        self.box = level.canvas.create_rectangle(x1 - BIRD_SIZE,
                                                 y1 - BIRD_SIZE,
                                                 x1, y1,
                                                 fill="gold1")
        self.falling_speed = 0

    def jump(self, foo):
        """Set a negative falling speed."""
        self.falling_speed = -3

    def weight(self):
        """Increase falling speed unless max then move it on canvas."""
        if self.falling_speed < MAX_FALL_SPEED:
            self.falling_speed += 0.1
        # Update position
        self.level.canvas.move(self.box, 0, self.falling_speed)


class Level:
    """Handle the game while the canvas is in use, including ticks."""

    def __init__(self, root):
        """Set up the canvas for the level.

        Makes a canvas the size of the window, makes a bird object inside it.
        Sets up the ground graphic, binds the space to the birds jump.
        Runs the tick method.
        """
        self.root = root
        canvas_height = self.root.winfo_height()  # Height canvas will be
        canvas_width = self.root.winfo_width()  # Width canvas will be
        self.canvas = tk.Canvas(self.root,
                                height=canvas_height,
                                width=canvas_width,
                                bg="green")
        self.canvas.pack()
        self.bird = Bird(self)  # Make the bird
        # Make the ground
        self.ground_box = self.canvas.create_rectangle(0,
                                                       canvas_height
                                                       - GROUND_HEIGHT,
                                                       canvas_width,
                                                       canvas_height,
                                                       fill="grey")
        self.root.bind('<space>', self.bird.jump)
        self.tick()

    def bird_is_not_touching(self):
        """Return True if the bird is not touching a pipe/the ground."""
        # First see if the bird is above the ground
        if self.canvas.coords(self.bird.box)[3] >= self.canvas.winfo_width()\
                - GROUND_HEIGHT:
            return False

        return True

    def tick(self):
        """Call methods that need to be called every tick."""
        print(self.bird_is_not_touching())
        self.bird.weight()
        self.canvas.after(MS_BETWEEN_TICKS, self.tick)


class TitleScreen:
    def __init__(self, root):
        self.root = root
        self.title_frame = tk.Frame(self.root)
        self.title_label = tk.Label(self.title_frame,
                                    text="Welcome to Flappy Bird")
        self.title_label.pack()
        self.play_button = tk.Button(self.title_frame,
                                     text="Play", command=self.play)
        self.play_button.pack()
        self.title_frame.pack()
        self.level = None

    def play(self):
        self.title_frame.pack_forget()
        self.level = Level(self.root)


class Game:
    def __init__(self):
        """Create a tk window, title screen object, and run mainloop."""
        self.root = tk.Tk()
        self.root.title("Flappy Bird - Matt Leith Edition")
        self.root.geometry("400x400")
        self.title_screen = TitleScreen(self.root)
        self.root.mainloop()


new_game = Game()
