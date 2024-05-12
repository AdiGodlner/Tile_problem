"""
This class represents the main window of the application, which contains tabs for
game options and gameplay. It initializes the GUI layout, handles messages between
the GUI and the solver process.

"""

import tkinter as tk
import ttkbootstrap as ttb
from GameTab import GameTab
from OptionsTab import OptionsTab
import queue


class Window(ttb.Window):
    """
    Window class represents the main application window.

    Attributes:
    - solver_to_gui_queue: A queue for messages from the solver process to the GUI.
    - gui_to_solver_queue: A queue for messages from the GUI to the solver process.
    - title: A string representing the title of the window.
    - theme_name: A string representing a ttkbootstrap theme for the GUI.
    - notebook: A ttkbootstrap.Notebook widget to hold tabs.
    - options_tab: An instance of OptionsTab representing the options tab.
    - game_tab: An instance of GameTab representing the game tab.
    """

    def __init__(self, gui_to_solver_queue, solver_to_gui_queue, process_interrupt_event,
                 title, theme_name):
        """
        Initializes the Window.

        Args:
        - gui_to_solver_queue: A queue for messages from the GUI to the solver process.
        - solver_to_gui_queue: A queue for messages from the solver process to the GUI.
        - process_interrupt_event: An event to interrupt the solver process.
        - title: A string representing the title of the window.
        - theme_name: A string representing a ttkbootstrap theme for the GUI.

        Initializes the window layout, creates tabs for options and gameplay,
        and sets up event binding for tab changes.
        """
        super().__init__(themename=theme_name)
        self.solver_to_gui_queue = solver_to_gui_queue
        self.gui_to_solver_queue = gui_to_solver_queue
        self.title = title
        self.theme_name = theme_name

        # Set the window size to fill the entire screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")

        # Create notebook widget to hold tabs
        self.notebook = ttb.Notebook(self)
        self.options_tab = OptionsTab(self.notebook, self.theme_name, self.set_theme)
        self.game_tab = GameTab(self.notebook, self.options_tab.get_option, self.gui_to_solver_queue,
                                process_interrupt_event)

        self.createLayout()

    def createLayout(self):
        """
        Creates the window layout.

        Creates the header label, adds tabs to the notebook,
        and sets up event bindings for tab changes.
        """
        # Create header label
        header_label = ttb.Label(self, text="Tile Game Solver",
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

    def set_theme(self, theme_name):
        """
        Sets the theme for the GUI.

        Args:
        - theme_name: A string representing a ttkbootstrap theme for the GUI.
        """
        self.style.theme_use(theme_name)

    def processIncoming(self):
        """
        Handles messages from the solver process.

        This method processes all messages currently in the solver_to_GUI queue,
        updating the game tab accordingly.
        """
        while self.solver_to_gui_queue.qsize():
            try:
                msg = self.solver_to_gui_queue.get_nowait()
                self.game_tab.process_incoming(msg)
            except queue.Empty:
                # Handle empty queue
                pass


def on_tab_changed(event):
    """
    Event handler for tab changing.

    Args:
    - event: The event object containing information about the event.
    """
    notebook_widget = event.widget
    # Get the name of the currently selected tab
    current_tab = notebook_widget.select()
    tab_object = notebook_widget.nametowidget(current_tab)
    # Call tab on_view function
    tab_object.on_view()
