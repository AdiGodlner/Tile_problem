"""
Provides the GameTab class representing a tab for displaying game-related information.

Classes:
    - GameTab: Represents a tab for displaying game-related information.

"""

from AbstractTab import Tab
from GamesFrame import GamesFrame
from ScoreFrame import ScoreFrame


class GameTab(Tab):
    """
    Represents a tab for displaying game-related information.

    Attributes:
        parent: The parent widget.
        get_options: A function to get options from the GUI.
        gui_to_solver_queue: A queue for communication between the GUI and the solver.
        tiles_solver_interrupt_event: An event for interrupting the solver.
        score_space: The score frame for displaying scores.
        game_space: The games frame for displaying game boards.
    """

    def __init__(self, parent, get_options, gui_to_solver_queue, tiles_solver_interrupt_event):
        """
        Initializes a GameTab object.

        Args:
            parent: The parent widget.
            get_options: A function to get options from the GUI.
            gui_to_solver_queue: A queue for communication between the GUI and the solver.
            tiles_solver_interrupt_event: An event for interrupting the solver.
        """
        super().__init__(parent)
        self.gui_to_solver_queue = gui_to_solver_queue
        self.tiles_solver_interrupt_event = tiles_solver_interrupt_event
        self.get_options = get_options
        self.score_space = ScoreFrame(self)
        self.game_space = GamesFrame(self, self.gui_to_solver_queue, tiles_solver_interrupt_event,
                                     self.score_space.display_winning_msg, get_options)

        self.createLayout()

    def createLayout(self):
        """
        Creates the layout for the game tab.
        """
        # Split the frame into a games frame and a score frame
        self.game_space.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.score_space.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Set grid weights to make the columns resizable
        self.grid_columnconfigure(0, weight=2)  # The first column gets 2/3 of the available space
        self.grid_columnconfigure(1, weight=1)  # The second column gets 1/3 of the available space

    def on_view(self):
        """
        Handles actions when the tab is viewed.
        """

        size = self.get_options("size")
        if self.game_space.board_size != size:
            # Create a new board if the size of the board has changed
            self.game_space.board_size = size
            self.game_space.reset_game()

    def processIncoming(self, solution_msg):
        """
        Processes incoming messages.

        Args:
            solution_msg: The solution message to process.
        """
        self.game_space.processIncoming(solution_msg)
