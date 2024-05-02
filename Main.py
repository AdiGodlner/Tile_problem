from MultiprocessingClient import MultiprocessingClient


def main():
    client = MultiprocessingClient(title="Tile game solver")
    client.mainloop()


if __name__ == "__main__":
    main()
