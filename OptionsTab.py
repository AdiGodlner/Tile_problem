import tkinter as tk
from TilesSolver import ALGO_MAP
from AbstractTab import Tab
import ttkbootstrap as ttb


def get_algo_options():
    return ALGO_MAP.keys()


def get_themes():
    return ["cosmo",
            "flatly",
            "journal",
            "litera",
            "lumen",
            "minty",
            "pulse",
            "sandstone",
            "united",
            "yeti",
            "morph",
            "simplex",
            "cerculean",
            "solar",
            "superhero",
            "darkly",
            "cyborg",
            "vapor"]


class OptionsTab(Tab):

    def __init__(self, parent, theme, set_theme):
        super().__init__(parent)

        self.selected_algorithm = tk.StringVar(value="BFS")
        self.theme_var = tk.StringVar(value=theme)
        self.size_var = tk.IntVar(value=3)
        self.options = {"algo": self.selected_algorithm,
                        "theme": self.theme_var,
                        "size": self.size_var}
        self.set_theme = set_theme
        self.pad_y = 24
        self.pad_x = 24
        self.create_widgets()

    def on_view(self):
        pass

    def create_widgets(self):
        # Add padding to the frame
        self.grid(padx=20, pady=20)

        # Create search algorithms section with larger font size
        search_algorithms_label = ttb.Label(self, text="Search Algorithms:", font=("Helvetica", 24))
        search_algorithms_label.grid(row=0, column=0, sticky="w", pady=self.pad_y, padx=self.pad_x)

        # Create radio btn options for possible search algorithms with larger font size
        for i, option in enumerate(get_algo_options()):
            btn = ttb.Radiobutton(self, text=option,
                                  variable=self.selected_algorithm,
                                  value=option)  # Set font size for radio buttons
            btn.grid(row=i + 1, column=0, sticky="w", padx=self.pad_x,
                     pady=self.pad_y)  # Apply padding to all radio buttons

        # Create size selection section with larger font size
        size_label = ttb.Label(self, text="Size:", font=("Helvetica", 24))
        size_label.grid(row=0, column=2, sticky="w", pady=self.pad_y)  # Increase padding below
        size_spinbox = ttb.Spinbox(self, from_=2, to=10,
                                   textvariable=self.size_var, width=5, font=("Helvetica", 24))
        size_spinbox.grid(row=1, column=2, sticky="w", pady=self.pad_y, padx=self.pad_x)

        # Create theme selection section with larger font size
        theme_label = ttb.Label(self, text="Theme:", font=("Helvetica", 24))
        theme_label.grid(row=0, column=1, sticky="w", pady=self.pad_y, padx=self.pad_x)

        theme_menu = tk.Menubutton(self, textvariable=self.theme_var, font=("Helvetica", 20),
                                   padx=self.pad_x /2,pady=self.pad_y /2)
        theme_menu.grid(row=1, column=1, sticky="w", pady=self.pad_y, padx=self.pad_x)
        theme_menu_options = ttb.Menu(theme_menu)
        for theme in get_themes():
            theme_menu_options.add_radiobutton(label=theme,
                                               variable=self.theme_var,
                                               command=self.on_theme_change)

        theme_menu.config(menu=theme_menu_options)

        # Add padding between grid items
        for i in range(3):
            self.columnconfigure(i, pad=self.winfo_screenwidth() / 10)  # Add padding between columns

        # Add padding between grid items
        for i in range(3):
            self.columnconfigure(i, pad=self.winfo_screenwidth() / 10)  # Add padding between columns

    def on_theme_change(self):
        new_theme = self.theme_var.get()
        self.set_theme(new_theme)

    def get_option(self, option):
        return self.options.get(option).get()
