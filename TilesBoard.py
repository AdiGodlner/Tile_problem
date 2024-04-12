from Tile import Tile
import tkinter as tk
from math import copysign


class TilesBoard(tk.Frame):

    def __init__(self, parent, enabled, tile_width=2, tile_height=2):
        super().__init__(parent, width=400, height=400, bg="red")
        self.board = []
        self.enabled = enabled
        self.zero_tile = None
        self.board_size = 0
        self.start_pos = 150
        self.btn_size = 40
        self.gap = 20

    def calc_position(self, row, col):
        x = self.start_pos + (col * (self.btn_size + self.gap))
        y = self.start_pos + (row * (self.btn_size + self.gap))
        return x, y

    def create_board(self, board_size):

        board = []

        for row in range(board_size):
            board_row = []
            board.append(board_row)
            for col in range(board_size):

                number = row * board_size + col
                tileBtn = Tile(self, number, row, col, self.enabled, self.game_move)
                board_row.append(tileBtn)
                # skip placing 0 tile
                if number != 0:
                    x, y = self.calc_position(row, col)
                    tileBtn.place(x=x, y=y)
                else:
                    self.zero_tile = tileBtn

        self.board = board

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
        for i, row in enumerate(self.board):
            for j, tile in enumerate(row):
                if int(tile["text"]) != i * self.board_size + j:
                    return
        print("Congratulations! Puzzle solved!")

        for row in self.board:
            for tile in row:
                print(tile.number)

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
