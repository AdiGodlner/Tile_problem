import tkinter as tk


def button_clicked(event):
    button_id = event.widget.find_closest(event.x, event.y)[0]
    print(f"num {find_btn_by_id(button_id)}")
    # button_text = event.widget.itemcget(button_id, "text")
    # print(f"Button {button_text} clicked!")


def find_btn_by_id(btn_ID):
    for index, id in enumerate(my_mapping):
        if id == btn_ID:
            return index


class my_btn:

    def __init__(self, canvas, row, col):
        x1 = col * button_width
        y1 = row * button_height
        x2 = x1 + button_width
        y2 = y1 + button_height
        # Numbering the buttons
        button_text = row * columns + col + 1

        self.canvas_ID = canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray")
        self.text_ID = canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=button_text)
        canvas.tag_bind(self.canvas_ID, "<Button-1>", button_clicked)

    def get_canvas_id(self):
        return self.canvas_ID


# Create the main window
root = tk.Tk()

# Create a Canvas widget
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

# Define the dimensions of the grid
rows = 3
columns = 3
button_width = 90
button_height = 90
my_mapping = []
# Create a grid of buttons
for i in range(rows):
    for j in range(columns):
        tile = my_btn(canvas, i, j)
        my_mapping.append(tile.get_canvas_id())

root.mainloop()
