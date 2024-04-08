import ttkbootstrap as ttb


def get_algo_options():
    return ["BFS", "IDDFS", "Greedy", "A*"]


def get_themes():
    return ["cerulean",
            "cosmo",
            "cyborg",
            "darkly",
            "flatly",
            "journal",
            "litera",
            "lumen",
            "lux",
            "materia",
            "minty",
            "pulse",
            "sandstone",
            "simplex",
            "sketchy",
            "slate",
            "solar",
            "spacelab",
            "superhero",
            "united",
            "yeti"]


class OptionsTab(ttb.Frame):

    def __init__(self, parent, theme):
        super().__init__(parent)

        self.selected_algorithm = ttb.StringVar(value="BFS")
        self.theme_var = ttb.StringVar(value=theme)
        self.size_var = ttb.IntVar(value=3)
        self.options = {"algorithm": self.selected_algorithm,
                        "theme": self.theme_var,
                        "size": self.size_var}
        self.create_widgets()

    def on_view(self):
        pass

    def create_widgets(self):
        # Create search algorithms section
        search_algorithms_label = ttb.Label(self, text="Search Algorithms:")
        search_algorithms_label.grid(row=0, column=0, sticky="w")

        #  create radio btn options for possible search algorithms
        for i, option in enumerate(get_algo_options()):
            btn = ttb.Radiobutton(self, text=option,
                                  variable=self.selected_algorithm,
                                  value=option)
            btn.grid(row=i + 1, column=0, sticky="w")

        # Create size selection section
        size_label = ttb.Label(self, text="Size:")
        size_label.grid(row=0, column=2, sticky="w")
        size_spinbox = ttb.Spinbox(self, from_=2, to=10,
                                   textvariable=self.size_var, width=5)
        size_spinbox.grid(row=1, column=2, sticky="w")

        # Create theme selection section
        theme_label = ttb.Label(self, text="Theme:")
        theme_label.grid(row=0, column=1, sticky="w")

        theme_combobox = ttb.Combobox(self, textvariable=self.theme_var, values=get_themes())
        theme_combobox.grid(row=1, column=1, sticky="w")

    def get_option(self, option):
        return self.options.get(option).get()
