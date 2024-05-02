from Window import Window
import sys
import multiprocessing
import TilesSolver


class MultiprocessingClient(object):
    def __init__(self, *args, **kwargs):

        gui_to_solver_queue = multiprocessing.Queue()
        solver_to_gui_queue = multiprocessing.Queue()
        # Set up the GUI part
        self.window = Window(gui_to_solver_queue, solver_to_gui_queue, *args, **kwargs)
        self.running = True

        # Start process for solving tiles
        tiles_solver_process = multiprocessing.Process(target=TilesSolver.solve_tiles,
                                                       args=(gui_to_solver_queue, solver_to_gui_queue))
        tiles_solver_process.daemon = True
        tiles_solver_process.start()
        # Start the periodic call in the GUI to check the queue
        self.periodic_call()

    def mainloop(self):
        self.window.mainloop()

    def periodic_call(self):
        # check if computer has already solved the tiles board
        self.window.after(200, self.periodic_call)
        self.window.processIncoming()
        if not self.running:
            # TODO exit more gracefully
            sys.exit(1)

    def clear_queue(self):
        # TODO clear tiles solver queue
        pass


def foo():
    bar = 0
    for i in range(10000):
        for j in range(i):
            bar += j
            if i % 10000 == 0 and j % 1000:
                print(f"i {i} j {j}")

    print(f"bar {bar}")
