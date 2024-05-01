import tkinter as tk

LEFT_CLICK = "<Button-1>"


class Tile:
    def __init__(self, canvas, size, number, row, col, enabled, game_move):
        self.canvas = canvas
        self.number = number
        self.canvas_id = None
        self.text_id = None
        self.row = row
        self.col = col
        self.size = size

        self.game_move = game_move
        self.enabled = enabled
        if not enabled:
            pass
            # TODO draw as disabled ?
            # self.disable()

    def draw(self, x1, x2, y1, y2):
        self.canvas_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray")
        self.text_id = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=self.number)
        self.canvas.tag_bind(self.canvas_id, LEFT_CLICK, self.on_click)

    def move(self, move_x, move_y):
        self.canvas.move(self.canvas_id, move_x, move_y)
        self.canvas.move(self.text_id, move_x, move_y)
        self.canvas.update()

    def clear(self):
        self.canvas.delete(self.canvas_id)
        self.canvas.delete(self.text_id)

    def copy(self, dest_canvas, enabled=True):
        new_tile = Tile(dest_canvas, self.size,
                        self.number, self.row, self.col, enabled, self.game_move)
        return new_tile

    def disable(self):
        pass
        #  TODO disable
        # self.configure(state="disabled")

    def enable(self):
        pass
        #  TODO enable
        # self.configure(state="normal")

    def on_click(self, event):
        self.game_move(self)
