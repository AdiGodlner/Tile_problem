import copy
import tkinter as tk
from TilesBoard import TilesBoard


class GameTab(tk.Frame):

    def __init__(self, parent, get_options):
        super().__init__(parent)
        self.get_options = get_options
        self.user_board = TilesBoard(self, True)
        tk.Label(self, text="User").pack()
        self.user_board.pack(fill="both", expand=1)

        # self.computer_board = self.user_board.copy(self, False)
        self.computer_board = TilesBoard(self, False)
        tk.Label(self, text="Computer").pack()
        self.computer_board.pack(fill="both", expand=1)

    def on_view(self):
        # clear board
        self.user_board.clear_board()
        self.computer_board.clear_board()
        size = self.get_options("size")
        self.user_board.create_board(size)
        self.computer_board.copy_board(self.user_board)
        self.computer_board.place_board()
