"""This file is designed to run a game of flappy bird.

All of the config is under the Game class.
Made for Mr Gardiner (I think).
Finished on the 9th of May 2021 (I had an extension)
"""

__author__ = "Matthew Leith"
import tkinter as tk
import random
import inspect


class Bird:
    """Handle the movements and graphics of the bird."""

    def __init__(self, game):
        """Create the bird, initialise falling_speed."""
        self._game = game
        self._level = game.level
        self.box = game.level.canvas.create_rectangle(self._game.BIRD_FRONT
                                                      - self._game.BIRD_SIZE,
                                                      self._game.BIRD_IN_HEIGHT
                                                      - self._game.BIRD_SIZE,
                                                      self._game.BIRD_FRONT,
                                                      self._game.
                                                      BIRD_IN_HEIGHT,
                                                      fill=self.
                                                      _game.BIRD_COLOUR,
                                                      tags="bird")
        self._game.root.bind('<space>', self.jump)
        self._falling_speed = 0

    def jump(self, event):
        """Set a negative falling speed."""
        self._falling_speed = -3

    def weight(self):
        """Increase falling speed unless max then move it on canvas."""
        if self._falling_speed < self._game.MAX_FALL_SPEED:
            self._falling_speed += 0.1
        # Check if updating position would put the bird though roof
        if self._level.canvas.coords(self.box)[1] + self._falling_speed <= 0:
            self._falling_speed = 0  # Hits head on roof

        # Update position
        self._level.canvas.move(self.box, 0, self._falling_speed)


class Pipe:
    """Handle the movements of actions of the pipe."""

    def __init__(self, game):
        """Initialise attributes and make the canvas objects."""
        self._game = game
        self._canvas = game.level.canvas
        self.off_screen = False  # Set True once pipe is no longer seen
        self._has_been_passed = False  # When bird passes then set True
        self._game.root.update()  # Update canvas to get dimensions
        # Store the height and width of the canvas
        canvas_height = self._canvas.winfo_height()
        canvas_width = self._canvas.winfo_width()
        # Generate a random gap location
        self._dist_from_top = random.randint(0,
                                             int(canvas_height
                                                 - self._game.GAP_SIZE
                                                 - self._game.GROUND_HEIGHT))
        # Make the canvas objects for the upper and lower pipes
        self._upper_box = self._canvas.create_rectangle(canvas_width
                                                        + self._game.
                                                        PIPE_WIDTH,
                                                        0,
                                                        canvas_width
                                                        + 2*self._game.
                                                        PIPE_WIDTH,
                                                        self._dist_from_top,
                                                        fill=self.
                                                        _game.PIPE_COLOUR,
                                                        tags="pipeU")

        self._lower_box = self._canvas.create_rectangle(canvas_width
                                                        + self._game.
                                                        PIPE_WIDTH,
                                                        self._dist_from_top
                                                        + self._game.GAP_SIZE,
                                                        canvas_width
                                                        + 2*self._game.
                                                        PIPE_WIDTH,
                                                        canvas_height,
                                                        fill=self.
                                                        _game.PIPE_COLOUR,
                                                        tags="pipeL")

    def move(self):
        """Move pipe's upper and lower parts left, check if visible."""
        self._canvas.move(self._upper_box, -self._game.PIPE_SPEED, 0)
        self._canvas.move(self._lower_box, -self._game.PIPE_SPEED, 0)
        # Check if the pipe is still visible or has passed the bird
        if self.off_screen is False and \
                self._canvas.coords(self._upper_box)[2] < 0:
            self.off_screen = True
        elif self._has_been_passed is False and \
                self._canvas.coords(self._upper_box)[2] <= \
                self._game.BIRD_FRONT - self._game.BIRD_SIZE:
            self._has_been_passed = True
            self._game.score_point()

    def remove(self):
        """Delete the upper and lower pipe on the canvas."""
        self._canvas.delete(self._upper_box)
        self._canvas.delete(self._lower_box)


class Level:
    """Handle the game while the canvas is in use, including ticks."""

    def __init__(self, game):
        """Set up the canvas for the level.

        Make a canvas the size of the window, make a bird object inside.
        Sets up the ground graphic, binds the space to the birds jump.
        Runs the tick method.
        """
        self._over = False  # I.e. the game is still in progress
        self._game = game
        self._root = self._game.root  # Make it shorter to get to
        self._tick_n = 0  # To keep track of how many ticks have occurred
        self._root.update()
        # Store the height and width of the canvas
        canvas_height = self._root.winfo_height()
        canvas_width = self._root.winfo_width()
        self.canvas = tk.Canvas(self._root,
                                height=canvas_height,
                                width=canvas_width,
                                bg="green")
        self._bird = None  # Initialise the bird variable
        # Make the ground
        self._ground_box = self.canvas.create_rectangle(0,
                                                        canvas_height
                                                        - self._game.
                                                        GROUND_HEIGHT,
                                                        canvas_width,
                                                        canvas_height,
                                                        fill="grey")
        self._pipe_list = []

    def _bird_is_not_touching(self):
        """Return True if the bird is not touching a pipe/the ground."""
        bird_coords = self.canvas.coords(self._bird.box)
        # See if bird is colling with anything
        if len(self.canvas.find_overlapping(bird_coords[0], bird_coords[1],
                                            bird_coords[2], bird_coords[3]))\
                > 1:
            return False

        return True  # No collision so return True

    def end_level(self):
        """Unpack the canvas, set level_over to True."""
        self._over = True
        self.canvas.pack_forget()

    def start_level(self):
        """Get the level get to play again and start tick."""
        # Remove existing pipes
        for a_pipe in self._pipe_list:
            a_pipe.remove()  # Get pipe to remove the canvas objects
        self._pipe_list = []
        self._over = False
        self._tick_n = 0
        self.canvas.delete("bird")  # Clear the canvas
        self._bird = Bird(self._game)  # Make the bird
        self.canvas.pack()  # Re/pack the canvas
        self._tick()  # Start tick loop

    def _tick(self):
        """Call methods that need to be called every tick."""
        if self._bird_is_not_touching() is not True:
            self._game.player_died()

        self._bird.weight()

        # See if we need a new pipe
        if self._tick_n % \
                int(self._game.PIPE_DISTANCE/self._game.PIPE_SPEED) == 0:
            self._pipe_list.append(Pipe(self._game))

        # Move pipes and remove old ones
        new_pipe_list = []  # Make a new list to prevent index errors
        for a_pipe in self._pipe_list:
            a_pipe.move()  # Get the pipe to move
            if a_pipe.off_screen is False:
                new_pipe_list.append(a_pipe)  # Preserve a reference
            else:
                a_pipe.remove()  # Get pipe to remove the canvas objects
        self._pipe_list = new_pipe_list  # Update the list

        if self._over is False:
            self._tick_n += 1
            self.canvas.after(self._game.MS_BETWEEN_TICKS, self._tick)


class TitleScreen:
    """Handel the activities of the title screen."""

    def __init__(self, game):
        """Crate labels in a frame and a button and pack them."""
        self._game = game
        self._title_frame = tk.Frame(self._game.root)
        self._title_label = tk.Label(self._title_frame,
                                     text="Welcome to Flappy Bird")
        self._title_label.pack()
        self._score_label = tk.Label(self._title_frame, text="")
        self._score_label.pack()
        self._high_score_label = tk.Label(self._title_frame, text="")
        self._high_score_label.pack()
        self._play_button = tk.Button(self._title_frame,
                                      text="Play",
                                      command=self._game.play_level)
        self._play_button.pack()
        self._how_to_label = tk.Label(
            self._title_frame,
            text="\n\nHow to play: click play and use spacebar to jump.\n"
                 + "You get a point when the whole bird goes past a pipe.")
        self._how_to_label.pack()

    def open_title_screen(self):
        """Pack the title screen's frame and updates score label."""
        if self._game.score != -1:  # Update the score if the have one
            self._score_label["text"] = "Last score: {}".format(
                self._game.score)
            self._high_score_label["text"] = "High score: {}".format(
                self._game.high_score)
        self._title_frame.pack()

    def close_title_screen(self):
        """Unpack the title screen's frame."""
        self._game.root.update()
        self._title_frame.pack_forget()
        self._game.root.update()


class Game:
    """Home of all config. Responsible for swapping title and level."""

    # Config. Only use integers or tkinter colours! I will check!
    HEIGHT = 400
    WIDTH = 400
    BIRD_SIZE = 20  # Width and height of the square bird
    # Pixel between right edge of bird and left edge of canvas
    BIRD_FRONT = 90
    # Pixel from top of screen the bottom of the bird spawns
    BIRD_IN_HEIGHT = int(HEIGHT / 4)  # Init height of bird
    BIRD_COLOUR = "gold1"  # Fill colour of the bird
    MAX_FALL_SPEED = 10  # Pixels per tick of the bird
    GROUND_HEIGHT = 23  # Pixels ground is above from bottom of canvas
    GAP_SIZE = 100  # Pixel size of gap between the lower and upper pipe
    PIPE_DISTANCE = 250  # Pixels between pipes
    PIPE_WIDTH = 30  # Pixel width of the pipes
    PIPE_COLOUR = "gold1"  # Fill colour of the pipes
    PIPE_SPEED = 2  # Pixels the pipe moves per tick
    MS_BETWEEN_TICKS = 10  # Milliseconds between each tick

    def __init__(self):
        """Create a tk window, title screen object, and run mainloop."""
        self.root = tk.Tk()
        # Test that the config has been set up correctly
        passed_config_test, fail_reason = self._check_config()
        if not passed_config_test:
            print("Game failed to start, in config: ", fail_reason)
        else:
            self.root.title("Flappy Bird - Matt Leith Edition")
            self.root.geometry("{}x{}".format(self.WIDTH, self.HEIGHT))
            self.score = -1  # Not 0 to tell if we have played before
            self.high_score = 0
            self.level = Level(self)  # Create level object
            self._title_screen = TitleScreen(self)  # Create title screen
            self._title_screen.open_title_screen()  # Open title screen

            self.root.mainloop()

    def _check_config(self):
        for i, v in inspect.getmembers(self):
            if i.isupper():  # Config constant detected
                # Should be an integer
                if i not in ("BIRD_COLOUR", "PIPE_COLOUR"):
                    if not isinstance(v, int):
                        return False, "Number not an integer"
                # Should be a tkinter colour
                elif i in ("BIRD_COLOUR", "PIPE_COLOUR"):
                    try:
                        # I mean if it works it must be a colour
                        tk.Frame(self.root, background=v)
                    except tk.TclError as error:
                        return False, "Colour not a tk colour"

        return True, "nil"  # Passed the test, reason for fail is nil

    def score_point(self):
        """Add a point to the score, called by pipe object"""
        self.score += 1

    def play_level(self):
        """Close title screen, make new level object."""
        self.score = 0
        self._title_screen.close_title_screen()
        self.level.start_level()

    def player_died(self):
        """Set high score, end level, open title screen."""
        if self.score > self.high_score:
            self.high_score = self.score
        self.level.end_level()
        self._title_screen.open_title_screen()


if __name__ == '__main__':
    new_game = Game()
