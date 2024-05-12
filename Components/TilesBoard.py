"""
Provides the TilesBoard class representing a game board.

Classes:
    - TilesBoard: Represents a game board.
"""

import numpy as np
from Components.Tile import Tile
import tkinter as tk
import random


class TilesBoard(tk.Canvas):
    """
    Represents a game board.

    Attributes:
        name (str): The name of the board.
        enabled (bool): Indicates whether the board is enabled.
        check_solved (function): A function to check if the game is solved.
        board (numpy.ndarray): A numpy array representing the board.
        zero_tile (Tile): The tile representing the empty space.
        btn_size (int): The size of each tile.
        default_total_frames (int): The default number of frames for animation.
        distance_per_frame (float): The distance to move per frame for animation.
    """

    def __init__(self, parent, name, enabled, check_solved):
        """
        Initializes a TilesBoard object.

        Args:
            parent: The parent widget.
            name (str): The name of the board.
            enabled (bool): Indicates whether the board is enabled.
            check_solved (function): A function to check if the game is solved.
        """
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
        """
        Copies the board.

        Args:
            original_tiles_board (TilesBoard): The original TilesBoard object to copy from.
        """
        original_board = original_tiles_board.board
        new_board = np.empty_like(original_board)

        for i, row in enumerate(original_board):
            for j, tile in enumerate(row):
                new_board[i, j] = tile.copy(self, self.enabled)
                if tile.number == 0:
                    self.zero_tile = new_board[i, j]

        self.board = new_board
        self.board_id = original_tiles_board.board_id

    def enable(self):
        """ Enables the board. """
        for row in self.board:
            for tile in row:
                tile.enable()

    def disable(self):
        """ Disables the board. """
        for row in self.board:
            for tile in row:
                tile.disable()

    def create_board(self, board_size):
        """
        Creates the game board.

        Args:
            board_size (int): The size of the game board.
        """
        num_board = generate_num_board(board_size)
        self.board = self.num_board_to_tiles(num_board)
        self.board_id = np.array2string(num_board)
        self.place_board()

    def num_board_to_tiles(self, num_board):
        """
        Converts an integer board to a board with tile objects.

        Args:
            num_board (numpy.ndarray): The integer representation of the game board.

        Returns:
            numpy.ndarray: A board with tile objects.
        """
        tiles_board = np.empty_like(num_board, dtype=object)

        for row_index, row in enumerate(num_board):

            for col, num in enumerate(row):

                tileBtn = Tile(self, self.btn_size, num, row_index, col, self.enabled, self.game_move)
                tiles_board[row_index, col] = tileBtn

                if num == 0:
                    self.zero_tile = tileBtn

        return tiles_board

    def get_num_board(self):
        """
         Retrieves the integer representation of the current game board.

         Returns:
             numpy.ndarray: The integer representation of the game board.
         """
        num_board = np.empty_like(self.board)

        for i, row in enumerate(self.board):

            for j, tile in enumerate(row):
                num_board[i, j] = tile.number

        return num_board

    def place_board(self):
        """
        Places the tiles of the board on the canvas.

        This method calculates the position of each tile on the canvas based on its row and column,
        then draws each tile on the canvas accordingly.

        """
        tile_size = self.board[0, 0].size
        board_start = (self.winfo_width() - (self.board.shape[0] * tile_size)) / 2

        for row in self.board:
            for tile in row:

                if tile.number != 0:
                    x1 = board_start + (tile.col * tile_size)
                    y1 = tile.row * tile_size
                    x2 = x1 + tile_size
                    y2 = y1 + tile_size
                    tile.draw(x1, x2, y1, y2)

    def game_move(self, tile):
        """
        Plays a move in the game.

        This method is called when a tile is clicked. It determines if the clicked tile can be moved,
        animates the movement of the tile, updates its position, updates the board matrix, and checks
        if the puzzle is solved after the move.

        :param tile: The tile to be moved.
        """
        row = tile.row
        col = tile.col
        zero_row = self.zero_tile.row
        zero_col = self.zero_tile.col
        row_diff = zero_row - row
        col_diff = zero_col - col

        if abs(row_diff) + abs(col_diff) == 1:
            self.animate_move(tile, col_diff, row_diff, self.default_total_frames)

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
        """
        Animates the movement of a tile.

        This method animates the movement of a tile by incrementally moving it in the specified direction
        over a series of frames.

        :param tile: The tile to be moved.
        :param x_direction: The direction of movement along the x-axis (-1 for left, 1 for right).
        :param y_direction: The direction of movement along the y-axis (-1 for up, 1 for down).
        :param total_frames: The total number of frames for the animation.
        """
        if total_frames > 0:
            move_x = self.distance_per_frame * x_direction
            move_y = self.distance_per_frame * y_direction

            # Move the tile by the calculated amount
            tile.move(move_x, move_y)

            # Schedule the next frame of animation
            self.after(10,
                       lambda TILE=tile, X_DIRECTION=x_direction, Y_DIRECTION=y_direction,
                              TOTAL_FRAMES=total_frames - 1
                       : self.animate_move(TILE, X_DIRECTION, Y_DIRECTION, TOTAL_FRAMES))

    def num_to_tiles_mapping(self):
        """
        Creates a mapping of tile numbers to tile objects.

        This method generates a mapping of tile numbers to their corresponding tile objects
        on the game board.

        :return: A NumPy array where each index represents a tile number and its value is the corresponding tile object.
        """
        num_to_tiles = np.empty(self.board.size, dtype=object)
        for row in self.board:
            for tile in row:
                num_to_tiles[tile.number] = tile

        return num_to_tiles

    def clear_board(self):
        """
        Clears the game board.

        This method clears the game board by removing all tile objects from the canvas and resetting the board attribute
        to None.

        """
        for row in self.board:
            for tile in row:
                tile.clear()

        self.board = None


def generate_num_board(board_size):
    """
    Generates a random yet solvable game board.

    This function generates a random game board of the specified size while ensuring that
     the generated board is solvable.

    Args:
        board_size (int): The size of the game board (e.g., 3 for a 3x3 board).

    Returns:
        numpy.ndarray: A randomly generated yet solvable game board represented as a numpy array.

    """
    num_board = generate_goal_state(board_size)
    # make board random yet solvable by playing 100 random moves
    make_random_moves(num_board, board_size, 0, 0)
    return num_board


def generate_goal_state(board_size):
    """
    Generates the goal state of the game board.

    This function generates the goal state of the game board,
     which is a board with tiles arranged in ascending order
    starting from 0.

    Args:
        board_size (int): The size of the game board (e.g., 3 for a 3x3 board).

    Returns:
        numpy.ndarray: The goal state of the game board represented as a numpy array.

    """
    return np.arange(board_size * board_size).reshape((board_size, board_size))


def make_random_moves(board, board_size, zero_row, zero_col):
    """
    Makes random moves on the game board.

    This function makes random moves on the game board by swapping tiles to increase
     randomness while keeping the board solvable.

    Args:
        board (numpy.ndarray): The game board represented as a numpy array.
        board_size (int): The size of the game board (e.g., 3 for a 3x3 board).
        zero_row (int): The row index of the empty tile (0) on the game board.
        zero_col (int): The column index of the empty tile (0) on the game board.

    """
    for _ in range(100):
        possible_moves = find_possible_moves(board_size, zero_row, zero_col)
        random_move = random.choice(possible_moves)
        # swap tiles
        row = random_move[0]
        col = random_move[1]
        num = board[row, col]
        board[zero_row, zero_col] = num
        board[row, col] = 0
        zero_row = row
        zero_col = col


def find_possible_moves(board_size, zeroRow, zeroCol):
    """
    Generates a list of possible moves in a square game board.

    This function creates a list of possible moves in a square game board based on the current location of the empty
    space marked as 0. The location of the empty space is given by zeroRow and zeroCol.

    Args:
        board_size (int): The size of the game board (e.g., 3 for a 3x3 board).
        zeroRow (int): The row index of the empty tile (0) on the game board.
        zeroCol (int): The column index of the empty tile (0) on the game board.

    Returns:
        list of tuple: A list of tuples, where each tuple represents
         a position of a tile on the board that can be moved.

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
