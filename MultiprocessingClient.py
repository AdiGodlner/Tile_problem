from Window import Window
import queue
import sys
# import threading
import multiprocessing


class MultiprocessingClient(object):
    def __init__(self, *args, **kwargs):

        self.gui_to_solver_queue = multiprocessing.Queue()
        self.solver_to_gui_queue = multiprocessing.Queue()
        # Set up the GUI part
        self.window = Window(self.gui_to_solver_queue, self.solver_to_gui_queue, *args, **kwargs)
        self.running = True

        # Start process for solving tiles
        tiles_solver_process = multiprocessing.Process(target=self.solve_tiles,
                                                       args=(self.gui_to_solver_queue, self.solver_to_gui_queue))
        tiles_solver_process.daemon = True
        tiles_solver_process.start()
        # Start the periodic call in the GUI to check the queue
        self.periodic_call()

    def mainloop(self):
        self.window.mainloop()

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

    def solve_tiles(self, gui_to_solver_queue, solver_to_gui_queue):
        #  consumer for tile boards to solve
        while self.running:
            try:
                task = self.gui_to_solver_queue.get(timeout=1)
                # print(f"got task from GUI | in thread {threading.current_thread().ident}")
                # simulate complex calculation
                # TODO solve tiles
                foo()
                # print(f"finished solving telling GUI | in thread {threading.current_thread().ident} ")
                self.solver_to_gui_queue.put(f"result for task {task} ")
            except queue.Empty:
                pass


def foo():
    bar = 0
    for i in range(10000):
        for j in range(i):
            bar += j
            if i % 10000 == 0 and j % 1000:
                print(f"i {i} j {j}")

    print(f"bar {bar}")
