from Window import Window
import multiprocessing
from TilesSolver import TilesSolver


class MultiprocessingClient(object):
    def __init__(self, *args, **kwargs):
        # set up objects for multi process communication
        gui_to_solver_queue = multiprocessing.Queue()
        self.solver_to_gui_queue = multiprocessing.Queue()
        self.process_interrupt_event = multiprocessing.Event()
        # Set up the GUI part
        self.window = Window(gui_to_solver_queue, self.solver_to_gui_queue, self.process_interrupt_event, *args,
                             **kwargs)
        self.tilesSolver = TilesSolver(self.process_interrupt_event, gui_to_solver_queue, self.solver_to_gui_queue)
        # Start process for solving tiles
        tiles_solver_process = multiprocessing.Process(target=self.tilesSolver.solve_tiles)
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
