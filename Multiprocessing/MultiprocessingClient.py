"""
This class serves as the main controller for the GUI and communication between
the GUI and the solver process.
It initializes the GUI window, the solver process
and manages periodic calls to update the GUI.

"""

from UI.Window import Window
import multiprocessing
from Solver.TilesSolver import TilesSolver


class MultiprocessingClient(object):
    """
    MultiprocessingClient class manages the GUI and solver process communication.

    Attributes:
    - solver_to_gui_queue: A multiprocessing.Queue for messages from the solver process to the GUI.
    - process_interrupt_event: A multiprocessing.Event to interrupt the solver process.
    - window: An instance of the Window class representing the GUI window.
    - tilesSolver: An instance of the TilesSolver class for solving the tiles puzzle.
    """

    def __init__(self, title, theme_name):
        """
        Initializes the MultiprocessingClient.

        Args:
        - title: A string representing the title of the GUI window.
        - theme_name: A string representing a ttkbootstrap theme for the GUI.

        Initializes communication queues, sets up the GUI window and solver process,
        and starts the periodic call so that the GUI will check for messages from the solver process.
        """

        # Set up objects for multiprocess communication
        gui_to_solver_queue = multiprocessing.Queue()
        self.solver_to_gui_queue = multiprocessing.Queue()
        self.process_interrupt_event = multiprocessing.Event()

        # Set up the GUI part
        self.window = Window(gui_to_solver_queue, self.solver_to_gui_queue, self.process_interrupt_event, title,
                             theme_name)
        self.tilesSolver = TilesSolver(self.process_interrupt_event, gui_to_solver_queue, self.solver_to_gui_queue)

        # Start process for solving tiles
        tiles_solver_process = multiprocessing.Process(target=self.tilesSolver.solve_tiles)
        tiles_solver_process.daemon = True
        tiles_solver_process.start()

        # Start the periodic call in the GUI to check the queue
        self.periodic_call()

    def mainloop(self):
        """
        Starts the main event loop of the GUI window.
        """
        self.window.mainloop()

    def periodic_call(self):
        """
        Periodically tells the GUI to check for messages from the solver process.

        Calls the processIncoming method of the GUI window to process incoming messages.
        """
        self.window.after(200, self.periodic_call)
        self.window.processIncoming()
