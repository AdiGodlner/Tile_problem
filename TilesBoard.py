from Tile import Tile
import tkinter as tk
from math import copysign
import random


class TilesBoard(tk.Frame):

    def __init__(self, parent, enabled):
        super().__init__(parent, width=400, height=400, bg="red")
        self.parent = parent
        self.board = []
        self.enabled = enabled
        self.zero_tile = None
        self.start_pos = 150
        self.btn_size = 40
        self.gap = 20

    def copy_board(self, tiles_board_to_copy):

        board_copy = []
        # iterate through the rows of the original board
        for row in tiles_board_to_copy.board:
            # create a new list by copying the elements of each row
            new_row = []
            board_copy.append(new_row)
            for tile in row:
                new_row.append(tile.copy(self, self.enabled))

        self.board = board_copy

    def disable(self):
        for row in self.board:
            for tile in row:
                tile.disable()

    def calc_position(self, row, col):
        x = self.start_pos + (col * (self.btn_size + self.gap))
        y = self.start_pos + (row * (self.btn_size + self.gap))
        return x, y

    def create_board(self, board_size):

        num_board = generate_num_board(board_size)
        self.board = self.num_board_to_tiles(num_board)
        self.place_board()
        #

    def num_board_to_tiles(self, num_board):

        tiles_board = []
        for row_index, row in enumerate(num_board):

            tiles_row = []
            tiles_board.append(tiles_row)
            for col, num in enumerate(row):

                tileBtn = Tile(self, num, row_index, col, self.enabled, self.game_move)
                tiles_row.append(tileBtn)
                # skip placing 0 tile
                if num == 0:
                    self.zero_tile = tileBtn

        return tiles_board

    def place_board(self):

        for row in self.board:

            for tile in row:
                num = tile.number
                if num != 0:
                    x, y = self.calc_position(tile.row, tile.col)
                    tile.place(x=x, y=y)

    def game_move(self, tile):

        row = tile.row
        col = tile.col
        zero_row = self.zero_tile.row
        zero_col = self.zero_tile.col

        if abs(row - zero_row) + abs(col - zero_col) == 1:
            # animate tile moving in GUI
            # find zero tile and current tile positions
            curr_tile_x, curr_tile_y = self.calc_position(row, col)
            zero_tile_x, zero_tile_y = self.calc_position(zero_row, zero_col)
            x_direction = zero_tile_x - curr_tile_x
            x_direction = copysign(1, x_direction) if x_direction != 0 else 0
            y_direction = zero_tile_y - curr_tile_y
            y_direction = copysign(1, y_direction) if y_direction != 0 else 0
            # animate
            self.animate_move(tile, curr_tile_x, curr_tile_y,
                              zero_tile_x, zero_tile_y,
                              x_direction, y_direction)

            # update tile position
            tile.row = zero_row
            tile.col = zero_col

            self.zero_tile.col = col
            self.zero_tile.row = row

            # change position on board matrix
            self.board[row][col] = self.zero_tile
            self.board[zero_row][zero_col] = tile

            # After moving the tile, check if the puzzle is solved
            self.check_solved()

    def check_solved(self):
        # Check if all tiles are in their correct positions
        board_size = len(self.board)
        for i, row in enumerate(self.board):
            for j, tile in enumerate(row):
                number = tile["text"]
                if int(number) != (i * board_size) + j:
                    return

        print("Congratulations! Puzzle solved!")
        self.disable()

    def animate_move(self, tile, origin_x, origin_y, dest_x, dest_y, x_direction, y_direction):
        if origin_x != dest_x or origin_y != dest_y:
            step = 5
            new_place_x = origin_x + (step * x_direction)
            new_place_y = origin_y + (step * y_direction)
            tile.place(x=new_place_x, y=new_place_y)

            self.after(10,
                       lambda: self.animate_move(tile, new_place_x, new_place_y, dest_x, dest_y, x_direction,
                                                 y_direction))

    def clear_board(self):

        for row in self.board:
            for tile in row:
                tile.destroy()

        self.board = []


def generate_num_board(board_size):
    num_board = []
    # create the goal state of the board
    for row in range(board_size):

        board_row = []
        num_board.append(board_row)
        for col in range(board_size):
            number = row * board_size + col
            board_row.append(number)

    # make board random yet solvable by playing 100 random moves
    make_random_moves(num_board, board_size, 0, 0)
    return num_board


def make_random_moves(board, board_size, zero_row, zero_col):
    for _ in range(100):
        possible_moves = findPossibleMoves(board_size, zero_row, zero_col)
        random_move = random.choice(possible_moves)
        # swap tiles
        row = random_move[0]
        col = random_move[1]
        num = board[row][col]
        board[zero_row][zero_col] = num
        board[row][col] = 0
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
