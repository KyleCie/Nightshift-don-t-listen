from gui import Menu

while True:
    result = Menu.run()

    if result is None:
        exit(0)

    match result:

        case "start":
            print("Starting the game...")
            
        case "continue":
            print("Continuing the game...")

        case "settings":
            print("Opening settings...")

        case "quit":
            print("Exiting the application...")
            exit(0)

        case _:
            print(f"Unknown menu result: {result}")