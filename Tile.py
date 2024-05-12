LEFT_CLICK = "<Button-1>"


class Tile:
    """
    Represents a tile in the game board.

    Args:
        canvas (tk.Canvas): The canvas where the tile will be drawn.
        size (int): The size of the tile.
        number (int): The number displayed on the tile.
        row (int): The row index of the tile.
        col (int): The column index of the tile.
        enabled (bool): Indicates whether the tile is enabled or disabled.
        game_move (function): The function to call when the tile is clicked.

    Attributes:
        canvas (tk.Canvas): The canvas where the tile is drawn.
        number (int): The number displayed on the tile.
        canvas_id (int): The ID of the tile's canvas object.
        text_id (int): The ID of the tile's text object.
        row (int): The row index of the tile.
        col (int): The column index of the tile.
        size (int): The size of the tile.
        game_move (function): The function to call when the tile is clicked.
        enabled (bool): Indicates whether the tile is enabled or disabled.

    """

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

    def draw(self, x1, x2, y1, y2):
        """
        Draws the tile on the canvas.

        Args:
            x1 (int): The x-coordinate of the top-left corner of the tile.
            x2 (int): The x-coordinate of the bottom-right corner of the tile.
            y1 (int): The y-coordinate of the top-left corner of the tile.
            y2 (int): The y-coordinate of the bottom-right corner of the tile.

        """
        self.canvas_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray")
        self.text_id = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=self.number)
        self.canvas.tag_bind(self.canvas_id, LEFT_CLICK, self.on_click)
        self.canvas.tag_bind(self.text_id, LEFT_CLICK, self.on_click)

    def move(self, move_x, move_y):
        """
        Moves the tile on the canvas by the specified amount.

        Args:
            move_x (int): The amount to move the tile in the x-direction.
            move_y (int): The amount to move the tile in the y-direction.

        """
        self.canvas.move(self.canvas_id, move_x, move_y)
        self.canvas.move(self.text_id, move_x, move_y)
        self.canvas.update()

    def clear(self):
        """ Clears the tile from the canvas. """
        self.canvas.delete(self.canvas_id)
        self.canvas.delete(self.text_id)

    def copy(self, dest_canvas, enabled=True):
        """
        Creates a copy of the tile.

        Args:
            dest_canvas (tk.Canvas): The canvas where the copy will be drawn.
            enabled (bool): Indicates whether the copy should be enabled or disabled.

        Returns:
            Tile: The copy of the tile.

        """
        new_tile = Tile(dest_canvas, self.size,
                        self.number, self.row, self.col, enabled, self.game_move)
        return new_tile

    def disable(self):
        """ Disables the tile. """
        self.enabled = False
        self.canvas.itemconfig(self.canvas_id, fill="lightgray")

    def enable(self):
        """ Enables the tile. """
        self.enabled = True
        self.canvas.itemconfig(self.canvas_id, fill="#3da9f9")

    def on_click(self, event):
        """
        Handles the tile click event.

        Args:
            event: The event object.

        """
        if self.enabled:
            self.game_move(self)
