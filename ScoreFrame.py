"""
Provides the ScoreFrame class representing a frame for displaying scores.

Classes:
    - ScoreFrame: Represents a frame for displaying scores.
"""

import tkinter as tk
from tkinter import messagebox


class ScoreFrame(tk.Frame):
    """
    Represents a frame for displaying scores.

    Attributes:
        user_wins: The number of wins by the user.
        computer_wins: The number of wins by the computer.
        user_wins_label: A label displaying the number of wins by the user.
        computer_wins_label: A label displaying the number of wins by the computer.
    """

    def __init__(self, parent):
        """
        Initializes a ScoreFrame object.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent)
        self.user_wins = 0
        self.computer_wins = 0
        font = ("Helvetica", 24)
        self.user_wins_label = tk.Label(self, text="User wins: 0", font=font)
        self.user_wins_label.pack(pady=(72, 0))
        self.computer_wins_label = tk.Label(self, text="Computer wins: 0", font=font)
        self.computer_wins_label.pack()

    def display_winning_msg(self, winning_board):
        """
        Displays a winning message based on the winning board.

        Args:
            winning_board: The winning board.
        """
        if winning_board.name == "user":

            self.user_wins += 1
            self.user_wins_label.config(text=f"User wins: {self.user_wins}")
            message = "User wins!"

        else:

            self.computer_wins += 1
            self.computer_wins_label.config(text=f"Computer wins: {self.computer_wins}")
            message = "Computer wins!"

        messagebox.showinfo("Winner", message)
