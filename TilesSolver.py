"""
Sliding Tile Problem Solver

This script provides implementations of various search algorithms (BFS, IDDFS, GBFS, A*)
for solving sliding tile problems of different sizes
By default, it solves the 3x3 sliding tile problem based on user input
provided as command-line arguments.

"""

import argparse
import sys
import heapq
import TilesBoard
import numpy as np
import queue
from TilesSolverMsgs import TilesSolverSolution


def find_child_states(currState):
    """
    Finds child states by generating all possible states that can be reached from the current state
    by moving the zero tile.

    Parameters:
    - currState (numpy.ndarray): The current state of the sliding tile board.

    Returns:
    - list: A list of tuples (childState, childMove) representing child states and their corresponding moves.
    """
    childStates = []
    board_size = currState.shape[0]
    # find the coordinates of the zero tile
    zeroRow, zeroCol = find_zero(currState)
    possibleMoves = TilesBoard.find_possible_moves(board_size, zeroRow, zeroCol)

    # generate child states by making moves
    for move in possibleMoves:
        # create a deep copy of the current state to avoid modifying the original state
        childState = np.copy(currState)
        # make the move and get the value of the moved tile
        movedTileValue = make_move(childState, move, zeroRow, zeroCol)
        childStates.append((childState, movedTileValue))

    return childStates


def make_move(board, move, zeroRow, zeroCol):
    """
    Makes a move on the board by swapping the zero tile with the specified tile.

    Parameters:
    - board (numpy.ndarray): The current state of the sliding tile board.
    - move (tuple): The position of the tile to be moved.
    - zeroRow (int): The row index of the zero tile.
    - zeroCol (int): The column index of the zero tile.

    Returns:
    - int: The value of the tile that was moved.
    """

    board[zeroRow, zeroCol] = board[move[0], move[1]]
    board[move[0], move[1]] = 0
    return board[zeroRow, zeroCol]


def find_zero(board):
    return np.argwhere(board == 0)[0]


def BFS(board, interrupt_event):
    """
    Performs Breadth-First Search (BFS) for the sliding tile problem.

    Parameters:
    - board (numpy.ndarray): The current state of the sliding tile board.
    - interrupt_event (multiprocessing.Event): An event to interrupt the search process.

    Returns:
    - tuple: A tuple containing the path (list) and the total number of states evaluated during the search.
    """
    goal = TilesBoard.generate_goal_state(len(board))
    totalChecks = 0
    # a dict containing a state as key and a (parentState ,move ) tuple as value
    reached = {}
    # the queue contains tuples of states their parent and the tile that moved from parent
    # to the current state
    frontier = queue.Queue()
    # set initial frontier to the starting board state with None parent and None move
    frontier.put((board, None, None))

    while (not frontier.empty()) and (not interrupt_event.is_set()):

        currState, parent, parentMove = frontier.get()
        totalChecks += 1

        if np.array_equal(goal, currState):
            path = reconstruct_path(parent, parentMove, reached)
            return path, totalChecks

        # adding the current state to the reached dict
        # we convert the current state to a tuple because dictionary keys must be Hashable
        currStateTuple = state_to_tuple(currState)
        reached[currStateTuple] = (parent, parentMove)

        childStates = find_child_states(currState)
        # add child states to the frontier queue
        for childState, childMove in childStates:
            # we convert the childState to a tuple because dictionary keys must Hashable
            childStateTuple = state_to_tuple(childState)
            if childStateTuple not in reached:
                frontier.put((childState, currStateTuple, childMove))

    return None, totalChecks


def IDDFS(board, interrupt_event):
    """
     Performs Iterative Deepening Depth-First Search (IDDFS) for the sliding tile problem.

     Parameters:
     - board (numpy.ndarray): The current state of the sliding tile board.
     - interrupt_event (multiprocessing.Event): An event to interrupt the search process.

     Returns:
     - tuple: A tuple containing the path (list) and the total number of states evaluated during the search.
     """
    # reached set is added for faster lookup of reached states
    # even thou reached states are already saved to path this does not
    # increase the asymptotic memory consumption
    # because depthLimitedSearch makes sure that 'path' and 'reached' have the same elements
    goal = TilesBoard.generate_goal_state(len(board))
    reached = set()
    path = []
    depth = 0
    totalChecks = 0
    # IDDFS needs to stop somewhere if there is no solution so 30 seams as good as any
    while depth < 30 and (not interrupt_event.is_set()):

        foundSolution, currChecks = depth_limited_search(board, goal, path, reached, depth)
        depth += 1
        totalChecks += currChecks

        if foundSolution:
            return path, totalChecks

    # couldn't reach goal state from given board state
    return None, totalChecks


def depth_limited_search(currState, goal, path, reached, maxDepth):
    """
    Performs a depth-limited search to find a path from the current state to the goal state.

    :param currState: (numpy.ndarray) The current state of the 3*3 board.
    :param goal: (numpy.ndarray) The state of the 3*3 board we want to get to.
    :param path: (list) A list to insert the move order to once a path is found.
    :param reached: (set) A set of states that have been visited to prevent looping over states
        that have already been explored on the way to the current state.
    :param maxDepth: The maximum depth to explore in the search.
    :return: A tuple (foundSolution, totalChecks).
             foundSolution (bool): True if a solution is found and False otherwise.
             totalChecks (int): The total number of states checked during the search.
    """

    totalChecks = 1
    # check if the current state is the goal state
    if np.array_equal(goal, currState):
        return True, totalChecks
    # check if the maximum depth has been reached
    if maxDepth == 0:
        return False, totalChecks

    # convert the current state to a tuple because elements of a set must be hashable
    currStateTuple = state_to_tuple(currState)
    reached.add(currStateTuple)

    childStates = find_child_states(currState)
    # Explore child states
    for childState, childMove in childStates:
        # convert the childState to a tuple because elements of a set must be hashable
        childStateTuple = state_to_tuple(childState)
        # check if the child state has not been visited
        if childStateTuple not in reached:
            # recursively perform depth-limited search on the child state
            foundSolution, checks = depth_limited_search(childState, goal, path, reached, maxDepth - 1)
            totalChecks += checks

            # if a solution is found, update the path and return
            if foundSolution:
                path.insert(0, childMove)
                return foundSolution, totalChecks

    # we get here only if we didn't find the solution in any of the current state's descendants,
    # so before we exit we remove the current state from the path and reached states as we go back up the
    # graph to try a different route
    reached.remove(currStateTuple)
    return False, totalChecks


def GBFS(board, interrupt_event):
    """
    Performs Greedy Best-First Search (GBFS) for the sliding tile problem.

    Parameters:
    - board (numpy.ndarray): The current state of the sliding tile board.
    - interrupt_event (multiprocessing.Event): An event to interrupt the search process.

    Returns:
    - tuple: A tuple containing the path (list) and the total number of states evaluated during the search.
    """
    goal = TilesBoard.generate_goal_state(len(board))
    totalChecks = 0
    count = 0
    # a dict containing a state as key and a (parentState ,move ) tuple as value
    reached = {}
    frontier = []
    # heapq sorts elements in the min heap based on the first value of the tuple
    heapq.heappush(frontier, (heuristic(board), count, board, None, None))

    while (len(frontier) > 0) and (not interrupt_event.is_set()):

        _, _, currState, parent, parentMove = heapq.heappop(frontier)
        totalChecks += 1

        if np.array_equal(goal, currState):
            path = reconstruct_path(parent, parentMove, reached)
            return path, totalChecks
        # adding the current state to the reached dict
        # we convert the current state to a tuple because dictionary keys must be Hashable
        currStateTuple = state_to_tuple(currState)
        reached[currStateTuple] = (parent, parentMove)

        childStates = find_child_states(currState)
        # add child states to the frontier heap
        for childState, childMove in childStates:
            # we convert the childState to a tuple because dictionary keys must Hashable
            childStateTuple = state_to_tuple(childState)
            if childStateTuple not in reached:
                priority = heuristic(childState)
                # a count is added to the tuple that is inserted into frontier as a tiebreaker
                # in case of 2 child states with the same priority
                # as it does not matter which child is checked if they have the same priority
                count += 1
                heapq.heappush(frontier, (priority, count, childState, currStateTuple, childMove))

    return None, totalChecks


class Node:
    """
    this class wraps a state (self.state) with its parent (self.parent) the move from the parent
     to the current state (self.parentMove)
     the total cost of moves to get to this state (cost)
     and the priority(self.priority) of the node so that the AStar search algorithm could
     sort the Node in the min heap

     Nodes are sorted by their priority as seen in the __lt__ method

     the node class wraps the state with its parent the move from the parent to the state the cost
     to get to the state and its priority
    """

    def __init__(self, state, parent, parentMove, cost, priority):
        self.state = state
        self.parent = parent
        self.parentMove = parentMove
        self.cost = cost
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority


def AStar(board, interrupt_event):
    """
    Performs A* Search for the sliding tile problem.

    Parameters:
    - board (numpy.ndarray): The current state of the sliding tile board.
    - interrupt_event (multiprocessing.Event): An event to interrupt the search process.

    Returns:
    - tuple: A tuple containing the path (list) and the total number of states evaluated during the search.
    """
    goal = TilesBoard.generate_goal_state(len(board))
    totalChecks = 0
    # frontier is a min heap that contains a Node object
    frontier = []
    # heapq sorts elements in the min heap based on the priority of the node value of the tuple
    boardNode = Node(board, None, None, 0, heuristic(board))
    heapq.heappush(frontier, boardNode)
    # because this is a tree search I added a last minute stopping condition in case there isn't a solution
    while (len(frontier) > 0) and (not interrupt_event.is_set()):

        currStateNode = heapq.heappop(frontier)
        currState = currStateNode.state
        totalChecks += 1

        if np.array_equal(goal, currState):
            path = []
            # reconstruct path to starting node
            while currStateNode.parent is not None:
                move = currStateNode.parentMove
                path.insert(0, move)
                currStateNode = currStateNode.parent

            return path, totalChecks

        childStates = find_child_states(currState)
        # add child states to the frontier heap
        for childState, childMove in childStates:
            # the cost of any move is the cost of its parent + 1
            childCost = currStateNode.cost + 1
            priority = heuristic(childState) + childCost
            childNode = Node(childState, currStateNode, childMove, childCost, priority)
            heapq.heappush(frontier, childNode)

    # if we did not find the solution we exit
    return None, totalChecks


def heuristic(board):
    """
    Calculates a heuristic score for a sliding tile board.

    Parameters:
    - board (numpy.ndarray): The current state of the sliding tile board.

    Returns:
    - int: The heuristic score for the board.
    """
    score = 0
    for row in range(len(board)):
        for column in range(len(board)):  # assume square matrix
            currTile = board[row][column]
            if currTile == 0:
                # skip count for 0 tile
                continue
            currTileGoalRow = currTile // 3
            currTileGoalColumn = currTile % 3
            if row != currTileGoalRow:  # currTile is not in its goal row
                score += 1
            if column != currTileGoalColumn:  # currTile is not in its goal column
                score += 1

    return score


def reconstruct_path(parent, parentMove, reached):
    """
    Reconstructs the path from the initial state to the goal state based on the parent-child relationships.

    Parameters:
    - parent: The parent state from which the reconstruction begins.
    - parentMove (int): The move (the value of the tile) that led from the parent state to the current state.
    - reached (dict): A dictionary mapping states to their parent states and corresponding moves.

    Returns:
    - list: The reconstructed path from the initial state to the goal state.
    """
    path = []
    # continue reconstructing the path until reaching the initial state (parent is None)
    while parent is not None:
        # insert the move at the beginning of the path
        path.insert(0, parentMove)
        # move to the parent state for the next iteration
        parent, parentMove = reached.get(parent)

    return path


def state_to_tuple(state):
    """
    Converts a 2D board state represented as a NumPy array to a hashable tuple for set membership.

    Args:
        state (numpy.ndarray): The 2D board state to be converted.

    Returns:
        tuple: A hashable tuple representing the board state.
    """
    return tuple(map(tuple, state))


def search_and_print_result(board, funcName, searchFunc):
    """
    Prints the result of a search algorithm for the given board state.

    Parameters:
    - board (numpy.ndarray): The initial 2D board state.
    - funcName (str): The name of the search function being used.
    - searchFunc (function): The search function to execute.
    """
    print(funcName)
    dummy_event = DummyEvent()
    path, totalChecks = searchFunc(board, dummy_event)
    print(path)
    print(totalChecks)


def get_user_board():
    """
    Gets the initial state of the sliding tile board from the user as command line arguments.

    Returns:
    - numpy.ndarray: The 2D board representing the initial state.
    """
    # get the initial state of the board as a list of numbers from the user as command line arguments
    parser = argparse.ArgumentParser(description='A script that prints the result of 4'
                                                 ' types of search algorithms for the 3x3 sliding tiles problem')
    parser.add_argument('numbers', type=int, nargs='+', help='List of numbers')
    args = parser.parse_args()
    numbers = args.numbers

    # check that user input has exactly 9 integers
    if len(numbers) != 9:
        print(len(numbers))
        print("script must get 9 integers from 0 to 8 in any order as args")
        sys.exit()

    # Convert the list of numbers to a 2D board
    board = np.empty([3, 3])
    for i in range(3):
        for j in range(3):
            board[i, j] = numbers[j + i * 3]

    return board


ALGO_MAP = {"BFS": BFS, "IDDFS": IDDFS, "GBFS": GBFS, "A*": AStar}


class TilesSolver:
    """
    A class that solves sliding tile problems using various search algorithms.
    """

    def __init__(self, interrupt_event, gui_to_solver_queue, solver_to_gui_queue):
        self.interrupt_event = interrupt_event
        self.gui_to_solver_queue = gui_to_solver_queue
        self.solver_to_gui_queue = solver_to_gui_queue

    def solve_tiles(self):
        """
        Solves sliding tile problems based on the received tasks.
        """
        #  Consumer for tile boards to solve
        while True:
            try:
                task = self.gui_to_solver_queue.get(timeout=1)

                if self.interrupt_event.is_set():
                    # The event is to be set to interrupt a running calculation
                    # and not to prevent from a calculation to start running
                    self.interrupt_event.clear()

                print(f"Got task from GUI {task}")
                algo = ALGO_MAP.get(task.algo_name)
                solution, _ = algo(task.tiles_board, self.interrupt_event)

                if self.interrupt_event.is_set():
                    # Allow GUI to interrupt process again
                    print(f"Process interrupted {self.interrupt_event.is_set()}")
                    self.interrupt_event.clear()
                else:
                    self.solver_to_gui_queue.put(TilesSolverSolution(solution, task.board_id))

            except queue.Empty:
                pass


class DummyEvent:
    """
    A dummy class representing an event for testing purposes.

    This class mimics the behavior of an event object without implementing the full functionality.
    It is used for testing scenarios where an event object is required but not utilized in its entirety.
    """

    def __init__(self):
        super().__init__()

    def is_set(self):
        """
        Checks if the event is set.

        Note:
        This method cannot be made static as it is a mock of the multiprocessing Event.is_set() method.

        Returns:
        - bool: Always returns False, as this is a mock method for the multiprocessing Event.is_set() method.
        """
        return False


if __name__ == "__main__":
    _userBoard = get_user_board()
    # Run search algorithms and print the results as instructed
    search_and_print_result(_userBoard, "BFS", BFS)
    search_and_print_result(_userBoard, "IDDFS", IDDFS)
    search_and_print_result(_userBoard, "GBFS", GBFS)
    search_and_print_result(_userBoard, "AStar", AStar)
