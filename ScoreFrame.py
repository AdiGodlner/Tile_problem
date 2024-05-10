import tkinter as tk
from tkinter import messagebox


class ScoreFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.user_wins = 0
        self.computer_wins = 0

        self.user_wins_label = tk.Label(self, text="User wins: 0")
        self.user_wins_label.pack()
        self.computer_wins_label = tk.Label(self, text="Computer wins: 0")
        self.computer_wins_label.pack()

    def display_winning_msg(self, winning_board):
        if winning_board.name == "user":
            self.user_wins += 1
            self.user_wins_label.config(text=f"User wins: {self.user_wins}")
            message = "User wins!"
        elif winning_board.name == "computer":
            self.computer_wins += 1
            self.computer_wins_label.config(text=f"Computer wins: {self.computer_wins}")
            message = "Computer wins!"
        else:
            message = "It's a tie!"

        messagebox.showinfo("Winner", message)
