from Window import Window
from DaemonThreadPoolExecutor import DaemonThreadPoolExecutor
import queue
import sys
import threading


class ThreadedClient(object):
    def __init__(self, *args, **kwargs):

        self.gui_to_solver_queue = queue.Queue()
        self.solver_to_gui_queue = queue.Queue()
        # Set up the GUI part
        self.window = Window(self.gui_to_solver_queue, self.solver_to_gui_queue, *args, **kwargs)
        self.running = True

        # Thread pool
        # self.thread_pool = DaemonThreadPoolExecutor(max_workers=1)  # Adjust max_workers as needed
        # # Start thread for solving
        # self.thread_pool.submit(self.solve_tiles)
        threading.Thread(target=self.solve_tiles, daemon=True).start()
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

    def solve_tiles(self):
        #  consumer for tile boards to solve
        while self.running:
            try:
                task = self.gui_to_solver_queue.get(timeout=1)
                print(f"got task from GUI {task} | in thread {threading.current_thread().ident}")
                # simulate complex calculation
                # TODO solve tiles
                foo()
                # print(f"thread {threading.current_thread().ident} going to sleep ")
                # time.sleep(4)
                # print(f"thread {threading.current_thread().ident} wake up  ")
                print("finished solving telling GUI")
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
