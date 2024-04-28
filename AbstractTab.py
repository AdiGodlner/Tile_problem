from abc import ABC, abstractmethod
from tkinter import Frame


class Tab(ABC, Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    @abstractmethod
    def on_view(self):
        pass