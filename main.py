"""By Matthew Leith"""
import tkinter as tk
HEIGHT = 400
WIDTH = 400
BIRD_SIZE = 20  # Width and height of the square bird
x1 = 30  # Pixels between the right edge of bird and left edge of canvas
y1 = WIDTH/4  # Pixels from the top of the screen the bottom of the bird spawns
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
                                                 fill="gold1",
                                                 tags="bird")
        self.level.root.bind('<space>', self.jump)
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

    def __init__(self, game):
        """Set up the canvas for the level.

        Makes a canvas the size of the window, makes a bird object inside it.
        Sets up the ground graphic, binds the space to the birds jump.
        Runs the tick method.
        """
        self.over = False  # I.e. the game is still in progress
        self.game = game
        self.root = self.game.root  # Make it shorter to get to
        canvas_height = self.root.winfo_reqheight()  # Height canvas will be
        canvas_width = self.root.winfo_reqheight()  # Width canvas will be
        self.canvas = tk.Canvas(self.root,
                                height=canvas_height,
                                width=canvas_width,
                                bg="green")
        #print(canvas_width, canvas_height)
        self.bird = None  # Initialise the bird variable
        # Make the ground
        self.ground_box = self.canvas.create_rectangle(0,
                                                       canvas_height
                                                       - GROUND_HEIGHT,
                                                       canvas_width,
                                                       canvas_height,
                                                       fill="grey")

    def bird_is_not_touching(self):
        """Return True if the bird is not touching a pipe/the ground."""
        # First see if the bird is above the ground
        if self.canvas.coords(self.bird.box)[3] >= self.canvas.winfo_reqheight()\
                - GROUND_HEIGHT:
            return False

        return True

    def end_level(self):
        """Unpack the canvas, set level_over to True"""
        self.over = True
        self.canvas.pack_forget()

    def start_level(self):
        """Get the level get to play again and start tick"""
        self.over = False
        self.canvas.delete("bird")  # Clear the canvas
        self.bird = Bird(self)  # Make the bird
        self.canvas.pack()
        #print(self.canvas.winfo_height(), self.root.winfo_height())
        self.tick()

    def tick(self):
        """Call methods that need to be called every tick."""
        if self.bird_is_not_touching() is not True:
            self.end_level()
            self.game.player_died()

        self.bird.weight()
        if self.over is False:
            self.canvas.after(MS_BETWEEN_TICKS, self.tick)


class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.title_frame = tk.Frame(self.game.root)
        self.title_label = tk.Label(self.title_frame,
                                    text="Welcome to Flappy Bird")
        self.title_label.pack()
        self.score_label = tk.Label(self.title_frame,
                                    text="")
        self.score_label.pack()
        self.high_score_label = tk.Label(self.title_frame,
                                         text="")
        self.high_score_label.pack()
        self.play_button = tk.Button(self.title_frame,
                                     text="Play",
                                     command=self.game.play_level)
        self.play_button.pack()
        self.open_title_screen()

    def open_title_screen(self):
        """Pack the title screen's frame and updates score label"""
        if self.game.score != -1:  # Update the score if the have one
            self.score_label["text"] = "Last score: {}".format(
                self.game.score)
            self.high_score_label["text"] = "High score: {}".format(
                self.game.high_score)
        self.title_frame.pack()

    def close_title_screen(self):
        """Unpack the title screen's frame"""
        self.game.root.update()
        self.title_frame.pack_forget()
        self.game.root.update()


class Game:
    def __init__(self):
        """Create a tk window, title screen object, and run mainloop."""
        self.root = tk.Tk()
        self.root.title("Flappy Bird - Matt Leith Edition")
        self.root.geometry("400x400")
        self.score = -1  # Not 0 to tell if we have played before
        self.high_score = 0
        self.level = Level(self)
        self.title_screen = TitleScreen(self)

        self.root.mainloop()

    def play_level(self):
        """Close title screen, make new level object"""
        self.score = 0
        self.title_screen.close_title_screen()
        self.level.start_level()

    def player_died(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.level.end_level()
        self.title_screen.open_title_screen()


new_game = Game()
