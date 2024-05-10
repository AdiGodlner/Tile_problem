from MultiprocessingClient import MultiprocessingClient


def main():
    client = MultiprocessingClient(title="Tile game solver", theme_name="superhero")
    client.mainloop()


if __name__ == "__main__":
    main()
