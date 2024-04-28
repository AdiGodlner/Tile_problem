from Window import Window
from concurrent.futures import ThreadPoolExecutor
import queue
import sys


class ThreadedClient(object):
    def __init__(self, *args, **kwargs):

        self.tiles_solver_queue = queue.Queue()
        # Set up the GUI part
        self.window = Window(queue, *args, **kwargs)
        self.running = True

        # Thread pool
        self.thread_pool = ThreadPoolExecutor(max_workers=1)  # Adjust max_workers as needed
        # Start thread for solving
        self.thread_pool.submit(self.solve_tiles)

        # Start the periodic call in the GUI to check the queue
        self.periodic_call()

    def periodic_call(self):
        # TODO check if computer has already solved the tiles board
        self.window.after(200, self.periodic_call)
        self.window.processIncoming()
        if not self.running:
            # TODO exit more gracefully
            sys.exit(1)

    def clear_queue(self):
        # TODO clear tiles solver queue
        pass

    def solve_tiles(self):
        #  consumer for tile boards to solve
        while self.running:
            try:
                task = self.tiles_solver_queue.get(timeout=1)
                print(task)
                # TODO solve tiles
            except queue.Empty:
                pass


client = ThreadedClient()
