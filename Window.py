import tkinter as tk
from tkinter import ttk
from GameTab import GameTab
from OptionsTab import OptionsTab
import threading

class Window(tk.Tk):
    def __init__(self,gui_to_solver_queue, solver_to_gui_queue, *args, **kwargs):
        super().__init__()
        self.solver_to_gui_queue = solver_to_gui_queue
        self.gui_to_solver_queue = gui_to_solver_queue
        self.title = kwargs.get("title")
        self.theme_name = kwargs.get("themename")
        # Set the window size to fill the entire screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        # Create notebook widget to hold tabs
        self.notebook = ttk.Notebook(self)
        self.createLayout()

    def createLayout(self):
        """
        Creates the window layout
        """
        # Create header label
        header_label = tk.Label(self, text="Tile Game Solver",
                                font=("Helvetica", 24))
        header_label.pack(pady=20)

        # Create tabs
        options_frame = OptionsTab(self.notebook, self.theme_name, self.set_theme)
        game_frame = GameTab(self.notebook, options_frame.get_option, self.gui_to_solver_queue)
        # testFrame = TestTab(self.notebook)

        options_frame.pack(fill="both", expand=1)
        game_frame.pack(fill="both", expand=1)
        # testFrame.pack(fill="both", expand=1)
        # Add tabs to notebook
        self.notebook.add(options_frame, text="Options")
        self.notebook.add(game_frame, text="Game")
        # self.notebook.add(testFrame, text="test")

        # Bind Tab changing event
        self.notebook.bind("<<NotebookTabChanged>>", on_tab_changed)
        # Pack notebook to fill window
        self.notebook.pack(fill=tk.BOTH, expand=True)

    def set_theme(self, theme):
        pass
        # self.style.theme_use(theme)

    def processIncoming(self):
        """ Handle all messages currently in the queue, if any. """
        while self.solver_to_gui_queue.qsize():
            try:
                print(f"in processIncoming thread {threading.current_thread().ident}")

                msg = self.solver_to_gui_queue.get_nowait()
                print(f"msg from solver : {msg}")
                # TODO process results from calculating threads
            except self.solver_to_gui_queue.Empty:
                # just in case
                # TODO check if this is nessacery
                pass


def on_tab_changed(event):
    notebook_widget = event.widget
    # Get the name of the currently selected tab
    current_tab = notebook_widget.select()
    tab_object = notebook_widget.nametowidget(current_tab)
    # call tab onView function
    tab_object.on_view()
