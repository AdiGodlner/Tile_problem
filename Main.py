from ThreadedClient import ThreadedClient


def main():
    client = ThreadedClient(title="Tile game solver")
    client.mainloop()


if __name__ == "__main__":
    main()
