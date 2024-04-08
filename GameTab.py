import ttkbootstrap as ttb

my_index = 1


class GameTab(ttb.Frame):

    def __init__(self, parent, get_options):
        super().__init__(parent)
        self.get_options = get_options
        # Create grid of numbers
        self.create_number_grid()

        # Create timer
        self.timer_label = ttb.Label(self, text="00:00", font=("Arial", 16))
        self.timer_label.grid(row=1, column=0, pady=10)

    def create_number_grid(self):
        size = self.get_options("size")
        for i in range(size):
            for j in range(size):
                label = ttb.Label(self, text=f"{i * size + j + 1}", font=("Arial", 12))
                label.grid(row=i + 2, column=j, padx=5, pady=5)

    def update_timer(self, time_str):
        self.timer_label.config(text=time_str)

    def on_view(self):
        self.create_number_grid()
