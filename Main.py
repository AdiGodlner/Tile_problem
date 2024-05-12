"""
Main file for the sliding tiles game solver application.

This script initializes and starts the MultiprocessingClient, which serves as the main GUI window
for the tile game solver application.
"""

from MultiprocessingClient import MultiprocessingClient


def main():
    """
    Creates an instance of MultiprocessingClient with specified title and theme,
    then starts the main event loop.
    """
    client = MultiprocessingClient(title="Tile game solver", theme_name="superhero")
    client.mainloop()


if __name__ == "__main__":
    main()
