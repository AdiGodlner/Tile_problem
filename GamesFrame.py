import tkinter as tk
from TilesSolverMsgs import TilesSolverTask
from TilesBoard import TilesBoard
import queue
import ttkbootstrap as ttb
from ttkbootstrap.constants import *


class GamesFrame(tk.Frame):

    def __init__(self, parent, gui_to_solver_queue, tiles_solver_interrupt_event, display_winning_msg,
                 get_options):
        super().__init__(parent, borderwidth=2)

        self.get_options = get_options
        self.display_winning_msg = display_winning_msg
        self.gui_to_solver_queue = gui_to_solver_queue
        self.tiles_solver_interrupt_event = tiles_solver_interrupt_event
        self.playing = False
        self.board_size = 0

        self.pad_y = 12
        self.pad_x = 12

        self.reset_btn = None
        self.start_btn = None

        self.user_board = TilesBoard(self, "user", False, self.check_solved)
        self.computer_board = TilesBoard(self, "computer", False, self.check_solved)
        self.createLayout()

    def createLayout(self):

        # Create a frame to contain the buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=self.pad_y)

        self.reset_btn = ttb.Button(button_frame, text="reset", command=self.reset_game, padding=(self.pad_x, self.pad_y))
        self.start_btn = ttb.Button(button_frame, text="start", command=self.start,
                                    padding=(self.pad_x, self.pad_y), bootstyle=SUCCESS)

        # Pack the buttons side by side in the button frame
        self.start_btn.pack(side=tk.LEFT, padx=self.pad_x)
        self.reset_btn.pack(side=tk.LEFT, padx=self.pad_x)

        self.reset_btn.pack()
        self.start_btn.pack()

        ttb.Label(self, text="User", font=("Helvetica", 24)).pack(pady=self.pad_y)
        self.user_board.pack(fill="both", expand=1)

        ttb.Label(self, text="Computer", font=("Helvetica", 24)).pack(pady=self.pad_y)
        self.computer_board.pack(fill="both", expand=1)

    def processIncoming(self, solution_msg):

        if self.user_board.board_id == solution_msg.board_id and self.playing:
            num_to_tiles = self.computer_board.num_to_tiles_mapping()

            for i, num in enumerate(solution_msg.solution):
                # insert events to main event loop to move the tiles so that it wont look like
                # the computer is cheating
                self.after(i * 100, lambda tile=num_to_tiles[num]: self.computer_board.game_move(tile))

    def reset_game(self):
        # if game is still in progress tell tiles solver to stop solving
        if self.playing:
            self.tiles_solver_interrupt_event.set()
            self.playing = False
        # enable start button
        self.start_btn.config(state="normal")
        # remove old boards from GUI
        self.computer_board.clear_board()
        self.user_board.clear_board()
        # create and place new Boards
        self.user_board.create_board(self.board_size)
        self.computer_board.copy_board(self.user_board)
        self.computer_board.place_board()

    def start(self):
        # disable start button
        self.start_btn.config(state="disabled")
        self.playing = True
        # remove other boards to solve from the queue if they exist
        self.clear_queue()
        self.user_board.enable()
        self.computer_play()

    def computer_play(self):
        # the search space for a 4x4 board is too big for my computer and may crash it,
        # so it has been limited for only user players
        if self.board_size <= 3:
            task = TilesSolverTask(self.get_options("algo"),
                                   self.computer_board.get_num_board(),
                                   self.computer_board.board_id)

            self.gui_to_solver_queue.put(task)

    def stop_game(self, winning_board):
        print(f"board : {winning_board.name} stopped the game ")
        print(f"self.user_board.name = {self.user_board.name}")
        print(f"self.computer_board.name = {self.computer_board.name}")
        if winning_board == self.user_board:
            print("user wins ")
            # stop computer if user has won
            self.tiles_solver_interrupt_event.set()

        if self.playing:
            self.playing = False
            self.user_board.disable()
            self.display_winning_msg(winning_board)

    def check_solved(self, tiles_board):
        # Check if all tiles are in their correct positions
        board = tiles_board.board
        board_size = len(board)
        for i, row in enumerate(board):
            for j, tile in enumerate(row):
                if int(tile.number) != (i * board_size) + j:
                    return False

        self.stop_game(tiles_board)
        # tiles_board.disable()
        return True

    def clear_queue(self):
        try:
            while not self.gui_to_solver_queue.empty():
                self.gui_to_solver_queue.get()
        except queue.Empty:
            pass
