import tkinter as tk


class Tile(tk.Button):
    def __init__(self, parent, number, row, col, enabled, game_move):
        super().__init__(parent, text=str(number),
                         width=2,
                         command=self.on_click)
        self.number = number
        self.row = row
        self.col = col
        self.game_move = game_move
        self.enabled = enabled
        # Create a label widget for the tile
        # Adjust the width and height of each tile
        # self.config(width=5, borderwidth=1, relief="raised", padding=10)
        # Bind click event to the label
        if not enabled:
            self.configure(state="disabled")

    def on_click(self):
        # print(f"clicked {self.number} | row {self.row}, col = {self.col} | enabled {self.enabled}")

        self.game_move(self)
