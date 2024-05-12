"""
Module: abstract_tab

Provides the Tab abstract class for defining tab interfaces in the GUI.

Classes:
    - Tab: Abstract base class representing a tab interface.

"""

from abc import ABC, abstractmethod
from tkinter import Frame


class Tab(ABC, Frame):
    """
    Abstract base class representing a tab interface.

    Attributes:
        parent: The parent widget.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initializes a Tab object.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent, *args, **kwargs)

    @abstractmethod
    def on_view(self):
        """
        Abstract method called when the tab is viewed.
        """
        pass
