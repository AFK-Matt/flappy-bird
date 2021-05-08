"""By Matthew Leith"""
__author__ = "Matthew Leith"

import tkinter as tk
import random


class Bird:
    """Handle the movements and graphics of the bird."""

    def __init__(self, game):
        """Create the bird, initialise falling_speed."""
        self.game = game
        self.level = game.level
        self.box = game.level.canvas.create_rectangle(self.game.BIRD_FRONT
                                                      - self.game.BIRD_SIZE,
                                                      self.game.BIRD_IN_HEIGHT
                                                      - self.game.BIRD_SIZE,
                                                      self.game.BIRD_FRONT,
                                                      self.game.BIRD_IN_HEIGHT,
                                                      fill="gold1",
                                                      tags="bird")
        self.level.root.bind('<space>', self.jump)
        self.falling_speed = 0

    def jump(self, event):
        """Set a negative falling speed."""
        self.falling_speed = -3

    def weight(self):
        """Increase falling speed unless max then move it on canvas."""
        if self.falling_speed < self.game.MAX_FALL_SPEED:
            self.falling_speed += 0.1
        # Check if updating position would put the bird though roof
        if self.level.canvas.coords(self.box)[1] + self.falling_speed <= 0:
            self.falling_speed = 0  # Hits head on roof

        # Update position
        self.level.canvas.move(self.box, 0, self.falling_speed)


class Pipe:
    """Handle the movements of actions of the pipe."""

    def __init__(self, game):
        """Initialise attributes and make the canvas objects"""
        self.game = game
        self.canvas = game.level.canvas
        self.off_screen = False  # Set True once pipe is no longer seen
        self.has_been_passed = False  # When the bird pass then set True
        # Store the height and width of the canvas
        canvas_height = self.canvas.winfo_reqheight()
        canvas_width = self.canvas.winfo_reqwidth()
        # Generate a random gap location
        self.dist_from_top = random.randint(0, int(canvas_height
                                                   - self.game.GAP_SIZE
                                                   - self.game.GROUND_HEIGHT))
        # Make the canvas objects for the upper and lower pipes
        self.upper_box = self.canvas.create_rectangle(canvas_width
                                                      + self.game.PIPE_WIDTH,
                                                      0,
                                                      canvas_width
                                                      + 2*self.game.PIPE_WIDTH,
                                                      self.dist_from_top,
                                                      fill=
                                                      self.game.PIPE_COLOUR,
                                                      tags="pipeU")

        self.lower_box = self.canvas.create_rectangle(canvas_width
                                                      + self.game.PIPE_WIDTH,
                                                      self.dist_from_top
                                                      + self.game.GAP_SIZE,
                                                      canvas_width
                                                      + 2*self.game.PIPE_WIDTH,
                                                      canvas_height,
                                                      fill=
                                                      self.game.PIPE_COLOUR,
                                                      tags="pipeL")

    def move(self):
        """Move the pipe upper and lower parts left, check if visible"""
        self.canvas.move(self.upper_box, -self.game.PIPE_SPEED, 0)
        self.canvas.move(self.lower_box, -self.game.PIPE_SPEED, 0)
        # Check if the pipe is still visible or has passed the bird
        if self.off_screen is False and \
                self.canvas.coords(self.upper_box)[2] < 0:
            self.off_screen = True
        elif self.has_been_passed is False and \
                self.canvas.coords(self.upper_box)[2] <= \
                self.game.BIRD_FRONT - self.game.BIRD_SIZE:
            self.has_been_passed = True
            print("Pipe passed")

    def remove(self):
        """Delete the upper and lower pipe on the canvas"""
        self.canvas.delete(self.upper_box)
        self.canvas.delete(self.lower_box)


class Level:
    """Handle the game while the canvas is in use, including ticks."""

    def __init__(self, game):
        """Set up the canvas for the level.

        Make a canvas the size of the window, make a bird object inside.
        Sets up the ground graphic, binds the space to the birds jump.
        Runs the tick method.
        """
        self.over = False  # I.e. the game is still in progress
        self.game = game
        self.root = self.game.root  # Make it shorter to get to
        self.tick_n = 0  # To keep track of how many ticks have occurred
        self.root.update()
        # Store the height and width of the canvas
        canvas_height = self.root.winfo_height()
        canvas_width = self.root.winfo_width()
        self.canvas = tk.Canvas(self.root,
                                height=canvas_height,
                                width=canvas_width,
                                bg="green")
        self.bird = None  # Initialise the bird variable
        # Make the ground
        self.ground_box = self.canvas.create_rectangle(0,
                                                       canvas_height
                                                       - self.game.
                                                       GROUND_HEIGHT,
                                                       canvas_width,
                                                       canvas_height,
                                                       fill="grey")
        self.pipe_list = []

    def bird_is_not_touching(self):
        """Return True if the bird is not touching a pipe/the ground."""
        bird_coords = self.canvas.coords(self.bird.box)
        # See if bird is colling with anything
        if len(self.canvas.find_overlapping(bird_coords[0], bird_coords[1],
                                            bird_coords[2], bird_coords[3]))\
                > 1:
            return False

        return True  # No collision so return True

    def end_level(self):
        """Unpack the canvas, set level_over to True"""
        self.over = True
        self.canvas.pack_forget()

    def start_level(self):
        """Get the level get to play again and start tick"""
        # Remove existing pipes
        for a_pipe in self.pipe_list:
            a_pipe.remove()  # Get pipe to remove the canvas objects
        self.pipe_list = []
        self.over = False
        self.tick_n = 0
        self.canvas.delete("bird")  # Clear the canvas
        self.bird = Bird(self.game)  # Make the bird
        self.canvas.pack()  # Re/pack the canvas
        self.tick()  # Start tick loop

    def tick(self):
        """Call methods that need to be called every tick."""
        if self.bird_is_not_touching() is not True:
            self.end_level()
            self.game.player_died()

        self.bird.weight()

        # See if we need a new pipe
        if self.tick_n % self.game.PIPE_DISTANCE == 0:
            self.pipe_list.append(Pipe(self.game))

        # Move pipes and remove old ones
        new_pipe_list = []  # Make a new list to prevent index errors
        for a_pipe in self.pipe_list:
            a_pipe.move()  # Get the pipe to move
            if a_pipe.off_screen is False:
                new_pipe_list.append(a_pipe)  # Preserve a reference
            else:
                a_pipe.remove()  # Get pipe to remove the canvas objects
        self.pipe_list = new_pipe_list  # Update the list

        if self.over is False:
            self.tick_n += 1
            self.canvas.after(self.game.MS_BETWEEN_TICKS, self.tick)


class TitleScreen:
    """Handel the activities of the title screen"""
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
    # Config
    HEIGHT = 400
    WIDTH = 400
    BIRD_SIZE = 20  # Width and height of the square bird
    BIRD_FRONT = 90  # Pixel between right edge of bird and left edge of canvas
    BIRD_IN_HEIGHT = WIDTH / 4  # Pixel from top of screen the bottom of the bird spawns
    BIRD_COLOUR = "gold1"
    MAX_FALL_SPEED = 10  # Pixels per tick of the bird
    MS_BETWEEN_TICKS = 10  # Milliseconds between each tick
    GROUND_HEIGHT = 23  # Pixels that the ground is above bottom of canvas
    GAP_SIZE = 100  # Pixel size of the gap between the lower and upper pipe
    PIPE_DISTANCE = 200  # Pixels between pipes
    PIPE_WIDTH = 30  # Pixel width of the pipes
    PIPE_COLOUR = "gold1"
    PIPE_SPEED = 1  # Pixels the pipe moves per tick

    def __init__(self):
        """Create a tk window, title screen object, and run mainloop."""
        self.root = tk.Tk()
        self.root.title("Flappy Bird - Matt Leith Edition")
        self.root.geometry("400x400")
        self.score = -1  # Not 0 to tell if we have played before
        self.high_score = 0
        self.level = Level(self)
        # Create title screen
        self.title_screen = TitleScreen(self)
        # Open title screen
        self.title_screen.open_title_screen()

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


if __name__ == '__main__':
    new_game = Game()
