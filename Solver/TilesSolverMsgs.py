"""
Provides classes for representing tasks and solutions in the TilesSolver.

Classes:
    - TilesSolverTask: Represents a task to be solved by the TilesSolver.
    - TilesSolverSolution: Represents a solution provided by the TilesSolver.
"""


class TilesSolverTask:
    """
    Represents a task to be solved by the TilesSolver.

    Attributes:
        algo_name (str): The name of the search algorithm to be used.
        tiles_board (numpy.ndarray): The initial state of the tiles board.
        board_id (int): The identifier of the board.
    """

    def __init__(self, algo_name, tiles_board, board_id):
        """
        Initializes a TilesSolverTask object.

        Args:
            algo_name (str): The name of the search algorithm to be used.
            tiles_board (numpy.ndarray): The initial state of the tiles board.
            board_id (int): The identifier of the board.
        """
        self.algo_name = algo_name
        self.tiles_board = tiles_board
        self.board_id = board_id


class TilesSolverSolution:
    """
    Represents a solution provided by the TilesSolver.

    Attributes:
        solution (list or None): The solution path or None if no solution is found.
        board_id (int): The identifier of the board associated with the solution.
    """

    def __init__(self, solution, board_id):
        """
        Initializes a TilesSolverSolution object.

        Args:
            solution (list or None): The solution path or None if no solution is found.
            board_id (int): The identifier of the board associated with the solution.
        """
        self.solution = solution
        self.board_id = board_id
