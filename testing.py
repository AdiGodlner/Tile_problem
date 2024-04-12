import tkinter as tk
from Tile import Tile


class tab(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="red", width=400, height=400)
        self.board = self.create_board()
        # self.btn1.pack()
        # self.btn1 = tk.Button(self, text="foo", command=self.up)
        # self.btn1 = Tile(self,10,0,0,True,self.up)
        # self.btn1.place(x=200, y=200, anchor="center")

    def create_board(self):

        board = []
        board_size = 3
        btn_size = 40
        gap = 20

        start_pos = 150

        for row in range(board_size):
            board_row = []
            board.append(board_row)
            for col in range(board_size):

                number = row * board_size + col
                tileBtn = Tile(self, number, row, col, True, self.move)
                board_row.append(tileBtn)
                # skip placing 0 tile
                if number != 0:
                    x = start_pos + (col * (btn_size + gap))
                    y = start_pos + (row * (btn_size + gap))
                    tileBtn.place(x=x, y=y, anchor="center")

        return board

    def move(self, tile):
        pass
        # if self.btn1y > 10:
        #     self.btn1y -= 10
        #     self.btn1.place(x=200, y=self.btn1y, anchor="center")
        #


root = tk.Tk()
root.geometry("800x800")
root.title("testing !!")

my_frame = tab(root)
# my_frame.place(x=400, y=400, anchor="center")
my_frame.pack()
root.mainloop()
