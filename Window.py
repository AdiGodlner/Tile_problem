import ttkbootstrap as ttb
from ttkbootstrap.constants import *
from tkinter import *
from GameTab import GameTab
from OptionsTab import OptionsTab


class Window(ttb.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.theme_name = kwargs.get("themename")
        # Set the window size to fill the entire screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        # Create notebook widget to hold tabs
        self.notebook = ttb.Notebook(self)
        self.createLayout()

    def createLayout(self):
        """
        Creates the window layout
        """
        # Create header label
        header_label = ttb.Label(self, text="Tile Game Solver",
                                 font=("Helvetica", 24))
        header_label.pack(pady=20)

        # Create tabs
        options_frame = OptionsTab(self.notebook, self.theme_name)
        game_frame = GameTab(self.notebook, options_frame.get_option)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Add tabs to notebook
        self.notebook.add(options_frame, text="Options")
        self.notebook.add(game_frame, text="Game")

        # Pack notebook to fill window
        self.notebook.pack(fill=ttb.BOTH, expand=True)

    def on_tab_changed(self, event):
        notebook_widget = event.widget
        # Get the name of the currently selected tab
        current_tab = notebook_widget.select()
        frame_object = notebook_widget.nametowidget(current_tab)
        # call tab onView function
        frame_object.on_view()