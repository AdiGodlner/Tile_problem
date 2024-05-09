import tkinter as tk


class TestTab(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, width=200, height=150)
        self.create_widgets()

    def create_widgets(self):
        game_space = tk.Frame(self)
        game_space.grid(row=0, column=0, sticky="nsew", padx=5,
                        pady=5)

        score_space = tk.Frame(self, bg="blue")
        score_space.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        # Set grid weights to make the columns resizable
        self.grid_columnconfigure(0, weight=2)  # The first column gets 2/3 of the available space
        self.grid_columnconfigure(1, weight=1)  # The second column gets 1/3 of the available space

    def on_view(self):
        pass
