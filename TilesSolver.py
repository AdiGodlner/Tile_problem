"""
3x3 sliding tile problem solver

This script provides implementations of 4 different search algorithms ( BFS, IDDFS, GBFS, A* )
 that solve the 3x3 sliding tile problem.
 the goal state the algorithms are trying to solve for is

    0  1  2
    3  4  5
    6  7  8

 as specified in the assignment sheet.
The initial state configuration is given by the user as a list of integers as cmd line argument
 as shown in the following example

Example:
python3 TilesSolver.py 0 6 4 7 3 5 1 2 8

"""
import argparse
import sys
import heapq
import TilesBoard
import numpy as np
import queue
from TilesSolverMsgs import TilesSolverTask, TilesSolverSolution


def findChildStates(currState):
    """
      finds child states by generating all possible states that can be reached from the current state
      by moving the zero tile.

    :param currState: (list of lists) The current state of the 3*3 board
    :return: a list of tuples (childState, childMove)
     where the child state is a state of the board after making the possible move childMove
     child move is the value of the tile that was moved e.g. 8
    """
    childStates = []
    board_size = currState.shape[0]
    # find the coordinates of the zero tile
    zeroRow, zeroCol = findZero(currState)
    possibleMoves = TilesBoard.findPossibleMoves(board_size, zeroRow, zeroCol)

    # generate child states by making moves
    for move in possibleMoves:
        # create a deep copy of the current state to avoid modifying the original state
        childState = np.copy(currState)
        # make the move and get the value of the moved tile
        movedTileValue = makeMove(childState, move, zeroRow, zeroCol)
        childStates.append((childState, movedTileValue))

    return childStates


def makeMove(board, move, zeroRow, zeroCol):
    """
    this function makes a move on the board by swapping the zero tile with the
    tile at the position specified by the coordinates in 'move'

    :param board: (list of lists) the current state of the 3*3 board
    :param move: (tuple) the position of the tile we want to move represented as a tuple (row, column)
    :param zeroRow: (int) the row in the board where zero is
    :param zeroCol: (int) the column in the board where zero is
    :return: (int) The value of the tile that was moved

    """

    board[zeroRow, zeroCol] = board[move[0], move[1]]
    board[move[0], move[1]] = 0
    return board[zeroRow, zeroCol]


def findZero(board):
    return np.argwhere(board == 0)[0]


def BFS(board, interrupt_event):
    """
    a graph search implementation of BFS (Breadth-First Search) for the 3*3 sliding tile problem
    this function finds an optimal path from a state 'board' to 'goalState'
    if it exists by preforming Breadth-First Search
    using legal sliding tile moves as described in the assignment

    :param board: (list of lists) the current state of the 3*3 board
    :return: the path (list) which is a list of the tile values that we need to move in order to get
    from the starting state to the goal state ( returns None if there is no such path )
    and an integer number of the number of states it evaluated until reaching that state
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
            path = reconstructPath(parent, parentMove, reached)
            return path, totalChecks

        # adding the current state to the reached dict
        # we convert the current state to a tuple because dictionary keys must be Hashable
        currStateTuple = stateToTuple(currState)
        reached[currStateTuple] = (parent, parentMove)

        childStates = findChildStates(currState)
        # add child states to the frontier queue
        for childState, childMove in childStates:
            # we convert the childState to a tuple because dictionary keys must Hashable
            childStateTuple = stateToTuple(childState)
            if childStateTuple not in reached:
                frontier.put((childState, currStateTuple, childMove))

    return None, totalChecks


def IDDFS(board, interrupt_event):
    """
    implementation of IDDFS (Iterative Deepening Depth-First Search) for the 3*3 sliding tile problem
    this function finds an optimal path from a state 'board' to 'goalState'
    if it exists by preforming Iterative Deepening Depth-First Search
    using legal sliding tile moves as described in the assignment

    :param board: (list of lists) the current state of the 3*3 board
    :return: the path (list) which is a list of the tile values that we need to move in order to get
    from the starting state to the goal state ( returns None if there is no such path )
    and an integer number of the number of states it evaluated until reaching that state
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

        foundSolution, currChecks = depthLimitedSearch(board, goal, path, reached, depth)
        depth += 1
        totalChecks += currChecks

        if foundSolution:
            return path, totalChecks

    # couldn't reach goal state from given board state
    return None, totalChecks


def depthLimitedSearch(currState, goal, path, reached, maxDepth):
    """
    performs a depth limited search to find a path from the current state to the goal state

    :param currState: (list of lists) the current state of the 3*3 board
    :param goal: (list of lists) the state of the 3*3 board we want to get to
    :param path: (list) a list to insert the move order to once a path is found
    :param reached: (set) a set of states that have been visited to prevent looping
     over states that have already been explored on the way to the current state
    :param maxDepth: the maximum depth to explore in the search
    :return: a tuple (foundSolution, totalChecks).
       foundSolution (bool): True if a solution is found and False otherwise
       totalChecks (int): The total number of states checked during the search
    """

    totalChecks = 1
    # check if the current state is the goal state
    if np.array_equal(goal, currState):
        return True, totalChecks
    # check if the maximum depth has been reached
    if maxDepth == 0:
        return False, totalChecks

    # convert the current state to a tuple because elements of a set must be hashable
    currStateTuple = stateToTuple(currState)
    reached.add(currStateTuple)

    childStates = findChildStates(currState)
    # Explore child states
    for childState, childMove in childStates:
        # convert the childState to a tuple because elements of a set must be hashable
        childStateTuple = stateToTuple(childState)
        # check if the child state has not been visited
        if childStateTuple not in reached:
            # recursively perform depth-limited search on the child state
            foundSolution, checks = depthLimitedSearch(childState, goal, path, reached, maxDepth - 1)
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
    implementation of GBFS (Greedy Best-First Search) for the 3*3 sliding tile problem
    this function finds a path from a state 'board' to 'goalState'
    if it exists by preforming Greedy Best-First Search
    using legal sliding tile moves as described in the assignment

   this function uses an admissible heuristic ( more detail in the documentation of the heuristic function )

    :param board: (list of lists) the current state of the 3*3 board
    :return: the path (list) which is a list of the tile values that we need to move in order to get
    from the starting state to the goal state ( returns None if there is no such path )
    and an integer number of the number of states it evaluated until reaching that state
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

        _,_, currState, parent, parentMove = heapq.heappop(frontier)
        totalChecks += 1

        if np.array_equal(goal, currState):
            path = reconstructPath(parent, parentMove, reached)
            return path, totalChecks
        # adding the current state to the reached dict
        # we convert the current state to a tuple because dictionary keys must be Hashable
        currStateTuple = stateToTuple(currState)
        reached[currStateTuple] = (parent, parentMove)

        childStates = findChildStates(currState)
        # add child states to the frontier heap
        for childState, childMove in childStates:
            # we convert the childState to a tuple because dictionary keys must Hashable
            childStateTuple = stateToTuple(childState)
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
    tree implementation of A* (A Star) for the 3*3 sliding tile problem
    this function finds a path from a state 'board' to 'goalState'
    if it exists by preforming A* search
    using legal sliding tile moves as described in the assignment

    this function uses an admissible heuristic ( more detail in the documentation of the heuristic function )

    :param board: (list of lists) the current state of the 3*3 board
    :return: the path (list) which is a list of the tile values that we need to move in order to get
    from the starting state to the goal state ( returns None if there is no such path )
    and an integer number of the number of states it evaluated until reaching that state
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

        childStates = findChildStates(currState)
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
    calculates a heuristic score for a sliding tiles board
    by counting the total number of tiles (excluding the 0 tile )
    not in their goal row + the total number of tiles not in their goal column
    this heuristic is admissible more details exist in the README.MD file

    :param board: (list of lists) the current state of the 3*3 board
    :return: (int) the heuristic score for the board
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


def reconstructPath(parent, parentMove, reached):
    """
    reconstructs the path from the initial state to the goal state based on the parent-child relationships.

    :param parent: (list of lists) the parent state from which the reconstruction begins
    :param parentMove: (int) the move (the value of the tile) that led from the parent state to the current state
    :param reached: A dictionary mapping states to their parent states and corresponding moves
    :return: (list) the reconstructed path  from the initial state to the goal state
    """
    path = []
    # continue reconstructing the path until reaching the initial state (parent is None)
    while parent is not None:
        # insert the move at the beginning of the path
        path.insert(0, parentMove)
        # move to the parent state for the next iteration
        parent, parentMove = reached.get(parent)

    return path


def transpose(board):
    """
    transpose a square matrix (2D list) representing a board

    Parameters:
    - board (list of lists): The square matrix to be transposed.

    Returns:
    - list of lists: .
    :param board: (list of lists) the original 2D board
    :return: (list of lists) the transposed matrix
    """
    lenBoard = len(board)
    return [[board[j][i] for j in range(lenBoard)] for i in range(lenBoard)]


def stateToTuple(state):
    """
     converts a 2D board state to a hashable tuple for set membership

    :param state:(list of lists) the 2D board state to be converted
    :return: a hashable tuple representing the board state
    """
    return tuple(map(tuple, state))


def searchAndPrintResult(board, funcName, searchFunc):
    """
     prints the 'funcName'
     performs a given search algorithm 'searchFunc'
     on a given board state 'board',  and prints the results of said search algorithm
     (the path and total checks) as instructed in the assignment paper

    :param board: (list of lists) the initial 2D board state
    :param funcName: (str) The name of the search function being used
    :param searchFunc: (function) The search function to execute
    """
    print(funcName)
    dummy_event = Dummy_event()
    path, totalChecks = searchFunc(board, dummy_event)
    print(path)
    print(totalChecks)


def getUserBoard():
    """
    gets the initial state of the 3x3 sliding tiles board from the user as command line arguments


    :return: (list of lists) the 2D board representing the initial state
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

    def __init__(self, interrupt_event, gui_to_solver_queue, solver_to_gui_queue):
        self.interrupt_event = interrupt_event
        self.gui_to_solver_queue = gui_to_solver_queue
        self.solver_to_gui_queue = solver_to_gui_queue

    def solve_tiles(self):
        #  consumer for tile boards to solve
        while True:
            try:
                task = self.gui_to_solver_queue.get(timeout=1)

                if self.interrupt_event.is_set():
                    # the event is to be set to interrupt a running calculation
                    # and not to prevent from a calculation to start running
                    self.interrupt_event.clear()

                print(f"got task from GUI {task}")
                algo = ALGO_MAP.get(task.algo_name)
                solution, _ = algo(task.tiles_board, self.interrupt_event)

                if self.interrupt_event.is_set():
                    # allow GUI to interrupt process again
                    print(f"process interrupted {self.interrupt_event.is_set()}")
                    self.interrupt_event.clear()
                else:
                    self.solver_to_gui_queue.put(TilesSolverSolution(solution, task.board_id))

            except queue.Empty:
                pass


class Dummy_event:
    def __init__(self):
        super().__init__()

    def is_set(self):
        return False


if __name__ == "__main__":
    _userBoard = getUserBoard()
    # _goalState = TilesBoard.generate_goal_state(len(_userBoard))
    # run search algorithms and print the results as instructed
    searchAndPrintResult(_userBoard, "BFS", BFS)
    searchAndPrintResult(_userBoard, "IDDFS", IDDFS)
    searchAndPrintResult(_userBoard, "GBFS", GBFS)
    searchAndPrintResult(_userBoard, "AStar", AStar)
