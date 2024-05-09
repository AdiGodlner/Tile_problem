import tkinter as tk
from tkinter import ttk
from GameTab import GameTab
from OptionsTab import OptionsTab
import queue


class Window(tk.Tk):
    def __init__(self, gui_to_solver_queue, solver_to_gui_queue, process_interrupt_event, *args, **kwargs):
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
        self.options_tab = OptionsTab(self.notebook, self.theme_name, self.set_theme)
        self.game_tab = GameTab(self.notebook, self.options_tab.get_option, self.gui_to_solver_queue,
                                process_interrupt_event)
        self.createLayout()

    def createLayout(self):
        """
        Creates the window layout
        """
        # Create header label
        header_label = tk.Label(self, text="Tile Game Solver",
                                font=("Helvetica", 24))
        header_label.pack(pady=20)

        self.options_tab.pack(fill="both", expand=1)
        self.game_tab.pack(fill="both", expand=1)
        # Add tabs to notebook
        self.notebook.add(self.options_tab, text="Options")
        self.notebook.add(self.game_tab, text="Game")

        # Bind Tab changing event
        self.notebook.bind("<<NotebookTabChanged>>", on_tab_changed)
        # Pack notebook to fill window
        self.notebook.pack(fill=tk.BOTH, expand=True)

    def set_theme(self, theme):
        pass
        # self.style.theme_use(theme)

    def processIncoming(self):
        """ Handle all messages currently in the queue, if any.
        this is here instead of games tab in case we would want to add
        different messages from process that are handled by different parts of the GUI
        """
        while self.solver_to_gui_queue.qsize():
            try:

                msg = self.solver_to_gui_queue.get_nowait()
                self.game_tab.processIncoming(msg)
            except queue.Empty:
                # just in case
                pass


def on_tab_changed(event):
    notebook_widget = event.widget
    # Get the name of the currently selected tab
    current_tab = notebook_widget.select()
    tab_object = notebook_widget.nametowidget(current_tab)
    # call tab onView function
    tab_object.on_view()
