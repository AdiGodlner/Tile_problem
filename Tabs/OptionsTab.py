"""
Provides the OptionsTab class for managing search algorithm options and themes in the GUI.

Classes:
    - OptionsTab: Represents a tab for configuring search algorithm options and themes.

Functions:
    - get_algo_options: Returns a list of available search algorithm options.
    - get_themes: Returns a list of available GUI themes.

"""

import tkinter as tk
import ttkbootstrap as ttb
from TilesSolver import ALGO_MAP
from AbstractTab import Tab


def get_algo_options():
    """
    Retrieves a list of available search algorithm options.

    Returns:
        list: A list of available search algorithm options.
    """
    return ALGO_MAP.keys()


def get_themes():
    """
    Retrieves a list of available GUI themes.

    Returns:
        list: A list of available GUI themes.
    """
    return [
        "cosmo", "flatly", "journal", "litera", "lumen", "minty", "pulse", "sandstone",
        "united", "yeti", "morph", "simplex", "cerculean", "solar", "superhero", "darkly",
        "cyborg", "vapor"
    ]


class OptionsTab(Tab):
    """
    Represents a tab for configuring search algorithm options and themes.

    Attributes:
        selected_algorithm (tk.StringVar): The selected search algorithm.
        theme_var (tk.StringVar): The selected GUI theme.
        size_var (tk.IntVar): The selected size for the board.
        options (dict): Dictionary containing configurable options.
        set_theme (function): Function for setting the GUI theme.
        pad_y (int): Vertical padding between widgets.
        pad_x (int): Horizontal padding between widgets.
    """

    def __init__(self, parent, theme_name, set_theme):
        """
        Initializes an OptionsTab object.

        Args:
            parent (tk.Tk or tk.Frame): The parent widget.
            theme_name: A string representing a ttkbootstrap theme for the GUI.
            set_theme (function): Function for setting the GUI theme.
        """
        super().__init__(parent)
        self.selected_algorithm = tk.StringVar(value="BFS")
        self.theme_var = tk.StringVar(value=theme_name)
        self.size_var = tk.IntVar(value=3)
        self.options = {"algo": self.selected_algorithm, "theme": self.theme_var, "size": self.size_var}
        self.set_theme = set_theme
        self.pad_y = 24
        self.pad_x = 24
        self.create_widgets()

    def on_view(self):
        """ Called when the tab is viewed. """
        pass

    def create_widgets(self):
        """
        Creates widgets for configuring search algorithm options and themes.
        """

        self.grid(padx=20, pady=20)

        search_algorithms_label = ttb.Label(self, text="Search Algorithms:", font=("Helvetica", 24))
        search_algorithms_label.grid(row=0, column=0, sticky="w", pady=self.pad_y, padx=self.pad_x)

        for i, option in enumerate(get_algo_options()):
            btn = ttb.Radiobutton(self, text=option, variable=self.selected_algorithm, value=option)
            btn.grid(row=i + 1, column=0, sticky="w", padx=self.pad_x, pady=self.pad_y)

        size_label = ttb.Label(self, text="Size:", font=("Helvetica", 24))
        size_label.grid(row=0, column=2, sticky="w", pady=self.pad_y)
        size_spinbox = ttb.Spinbox(self, from_=2, to=10, textvariable=self.size_var, width=5, font=("Helvetica", 24))
        size_spinbox.grid(row=1, column=2, sticky="w", pady=self.pad_y, padx=self.pad_x)

        theme_label = ttb.Label(self, text="Theme:", font=("Helvetica", 24))
        theme_label.grid(row=0, column=1, sticky="w", pady=self.pad_y, padx=self.pad_x)

        theme_menu = tk.Menubutton(self, textvariable=self.theme_var, font=("Helvetica", 20), padx=self.pad_x / 2,
                                    pady=self.pad_y / 2)
        theme_menu.grid(row=1, column=1, sticky="w", pady=self.pad_y, padx=self.pad_x)
        theme_menu_options = ttb.Menu(theme_menu)
        for theme in get_themes():
            theme_menu_options.add_radiobutton(label=theme, variable=self.theme_var, command=self.on_theme_change)

        theme_menu.config(menu=theme_menu_options)

        for i in range(3):
            self.columnconfigure(i, pad=self.winfo_screenwidth() / 10)

    def on_theme_change(self):
        """
        Called when the selected GUI theme is changed.
        """
        new_theme = self.theme_var.get()
        self.set_theme(new_theme)

    def get_option(self, option):
        """
        Retrieves the value of a specified option.

        Args:
            option (str): The name of the option.

        Returns:
            Any: The value of the specified option.
        """
        return self.options.get(option).get()

