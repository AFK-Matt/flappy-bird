"""By Matthew Leith"""
import tkinter as tk

root = tk.Tk()

root.title("Flappy Bird - Matt Leith Edition")
root.geometry("400x400")


class TitleScreen:
    def __init__(self):
        self.title_frame = tk.Frame(root)
        self.title_label = tk.Label(self.title_frame, text="Welcome to Flappy Bird")
        self.title_label.pack()
        self.play_button = tk.Button(self.title_frame, text="Play", command=self.play)
        self.play_button.pack()
        self.title_frame.pack()

    def play(self):
        self.title_frame.pack_forget()


def run_game():
    new_cress = TitleScreen()


run_game()
root.mainloop()


