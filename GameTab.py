import copy
import tkinter as tk
from TilesBoard import TilesBoard
import threading
from Tiles import ALGO_MAP
import numpy as np


class GameTab(tk.Frame):

    def __init__(self, parent, get_options):
        super().__init__(parent)
        self.playing = True
        self.get_options = get_options
        self.board_size = 0
        # game menu btns
        self.restart_btn = tk.Button(self, text="restart ", command=self.restart_game)
        self.restart_btn.pack()
        # user board
        tk.Label(self, text="User").pack()
        self.user_board = TilesBoard(self, "user", True, self.check_solved)
        self.user_board.pack(fill="both", expand=1)

        # computer board
        tk.Label(self, text="Computer").pack()
        self.computer_board = TilesBoard(self, "computer", False, self.check_solved)
        self.computer_board.pack(fill="both", expand=1)

    def on_view(self):
        # clear board
        size = self.get_options("size")

        if self.board_size != size:
            self.board_size = size
            self.restart_game()

    def restart_game(self):

        self.playing = True
        # remove old boards from GUI
        self.user_board.clear_board()
        self.computer_board.clear_board()
        # create and place new Boards
        self.user_board.create_board(self.board_size)
        self.computer_board.copy_board(self.user_board)
        self.computer_board.place_board()
        # let the computer play the game on a different thread to not interrupt the user
        threading.Thread(target=self.computer_play, daemon=True).start()

    def computer_play(self):
        print("in new thread ")
        num_board = self.computer_board.get_num_board()
        algo_name = self.get_options("algorithm")
        print(algo_name)
        algo = ALGO_MAP.get(algo_name)
        solution = algo(num_board)

        for num in solution:
            pass
            # TODO computer move

        self.stop_game(self.computer_board)

    def stop_game(self, winning_board):

        if self.playing:
            self.playing = False
            self.user_board.disable()
            self.display_winning_msg(winning_board)

    def display_winning_msg(self, winning_board):
        pass

    def check_solved(self, tiles_board):
        # Check if all tiles are in their correct positions
        board = tiles_board.board
        board_size = len(board)
        for i, row in enumerate(board):
            for j, tile in enumerate(row):
                number = tile["text"]
                if int(number) != (i * board_size) + j:
                    return False

        tiles_board.disable()
        return True
