import numpy as np

from Tile import Tile
import tkinter as tk
from math import copysign
import random


class TilesBoard(tk.Canvas):

    def __init__(self, parent, name, enabled, check_solved):
        super().__init__(parent, width=400, height=400, bg="white")
        self.parent = parent
        self.name = name
        self.board_id = None
        self.check_solved = check_solved
        self.board = np.array([])
        self.enabled = enabled
        self.zero_tile = None
        self.btn_size = 40
        self.default_total_frames = 10
        self.distance_per_frame = self.btn_size / self.default_total_frames

    def copy_board(self, original_tiles_board):

        original_board = original_tiles_board.board
        new_board = np.empty_like(original_board)

        for i, row in enumerate(original_board):
            for j, tile in enumerate(row):
                new_board[i, j] = tile.copy(self, self.enabled)

        self.board = new_board
        self.board_id = original_tiles_board.board_id

    def enable(self):
        for row in self.board:
            for tile in row:
                tile.enable()

    def disable(self):
        for row in self.board:
            for tile in row:
                tile.disable()

    def create_board(self, board_size):

        num_board = generate_num_board(board_size)
        self.board = self.num_board_to_tiles(num_board)
        self.board_id = np.array2string(num_board)
        self.place_board()

    def num_board_to_tiles(self, num_board):

        tiles_board = np.empty_like(num_board, dtype=object)

        for row_index, row in enumerate(num_board):

            for col, num in enumerate(row):

                tileBtn = Tile(self, self.btn_size, num, row_index, col, self.enabled, self.game_move)
                tiles_board[row_index, col] = tileBtn

                if num == 0:
                    self.zero_tile = tileBtn

        return tiles_board

    def get_num_board(self):

        board_size = len(self.board)
        num_board = np.empty_like(self.board)
        bored_tiles = np.zeros(board_size * board_size)

        for i, row in enumerate(self.board):

            for j, tile in enumerate(row):
                num_board[i, j] = tile.number
                bored_tiles[tile.number] = tile.number

        return num_board

    def place_board(self):

        for row in self.board:
            for tile in row:

                if tile.number != 0:
                    x1 = tile.col * tile.size
                    y1 = tile.row * tile.size
                    x2 = x1 + tile.size
                    y2 = y1 + tile.size
                    tile.draw(x1, x2, y1, y2)

    def game_move(self, tile):
        row = tile.row
        col = tile.col
        zero_row = self.zero_tile.row
        zero_col = self.zero_tile.col
        row_diff = zero_row - row
        col_diff = zero_col - col
        if abs(row_diff) + abs(col_diff) == 1:
            # TODO fix this to work with drawing on canvas
            # TODO does this need the copy sign ?
            x_direction = copysign(1, col_diff) if col_diff != 0 else 0
            y_direction = copysign(1, row_diff) if row_diff != 0 else 0

            self.animate_move(tile, x_direction, y_direction, self.default_total_frames)

            # update tile position
            tile.row = zero_row
            tile.col = zero_col

            self.zero_tile.col = col
            self.zero_tile.row = row

            # change position on board matrix
            self.board[row, col] = self.zero_tile
            self.board[zero_row, zero_col] = tile

            # After moving the tile, check if the puzzle is solved
            self.check_solved(self)

    def animate_move(self, tile, x_direction, y_direction, total_frames):
        if total_frames > 0:
            move_x = (self.distance_per_frame * x_direction)
            move_y = (self.distance_per_frame * y_direction)

            tile.move(move_x, move_y)
            self.after(10,
                       lambda TILE=tile, X_DIRECTION=x_direction, Y_DIRECTION=y_direction
                              , TOTAL_FRAMES=total_frames - 1
                       : self.animate_move(TILE, X_DIRECTION, Y_DIRECTION, TOTAL_FRAMES))

    def clear_board(self):

        for row in self.board:
            for tile in row:
                tile.clear()

        self.board = None


def generate_num_board(board_size):
    num_board = generate_goal_state(board_size)
    # make board random yet solvable by playing 100 random moves
    make_random_moves(num_board, board_size, 0, 0)
    return num_board


def generate_goal_state(board_size):
    return np.arange(board_size * board_size).reshape((board_size, board_size))


def make_random_moves(board, board_size, zero_row, zero_col):
    for _ in range(100):
        possible_moves = findPossibleMoves(board_size, zero_row, zero_col)
        random_move = random.choice(possible_moves)
        # swap tiles
        row = random_move[0]
        col = random_move[1]
        num = board[row, col]
        board[zero_row, zero_col] = num
        board[row, col] = 0
        zero_row = row
        zero_col = col


def findPossibleMoves(board_size, zeroRow, zeroCol):
    """
    this method creates a list of possible moves in a 3*3 board
    based on the current location of the empty space marked as 0
    the location of zero is given by zeroRow and zeroCol as mention below
    :param zeroRow: (int) the row in the board where zero is
    :param zeroCol: (int) the column in the board where zero is
    :return: a list of tuples each tuple is a position of a tile on the board that can be moved
    """
    possibleMoves = []
    if zeroRow != 0:
        # move zero up
        possibleMoves.append((zeroRow - 1, zeroCol))

    if zeroRow != board_size - 1:
        # move zero down
        possibleMoves.append((zeroRow + 1, zeroCol))

    if zeroCol != 0:
        # move zero left
        possibleMoves.append((zeroRow, zeroCol - 1))

    if zeroCol != board_size - 1:
        # move zero right
        possibleMoves.append((zeroRow, zeroCol + 1))

    return possibleMoves
