import tkinter as tk


class Tile(tk.Button):
    def __init__(self, parent, number, row, col, enabled, game_move):
        super().__init__(parent, text=str(number),
                         width=2,
                         command=self.on_click)
        self.parent = parent
        self.number = number
        self.canvas_id = None
        self.row = row
        self.col = col
        self.game_move = game_move
        self.enabled = enabled
        if not enabled:
            self.disable()

    def copy(self, parent, enabled=True):
        new_tile = Tile(parent, self.number, self.row, self.col, enabled, self.game_move)
        return new_tile

    def disable(self):
        self.configure(state="disabled")

    def enable(self):
        self.configure(state="normal")

    def on_click(self):
        self.game_move(self)
