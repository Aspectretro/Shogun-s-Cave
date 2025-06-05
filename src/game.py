from map import Map
from item import Item
from cave import Cave
from character import Character
import random as r

class Game:
    """Class that manages all aspects of a currently running session, including the player 

    All other classes are managed by an instance of this class
    """
    def __init__(self):
        self.alive = True

        # Generate map
        self.map = Map()
        self.map.generate()

        self.current_cave = self.map.starting_cave # initially the player begins in the starting cave
    
    def tutorial(self):
        # TODO: tutorial
        """Start the tutorial for the game. Does not begin the main game loop"""

        print("\n")
        print("Welcome to [game name]! This is the tutorial and will show you how the game works.")
        print("If you are already familiar with the game, enter q to skip.")
        print("\n")

        print("This arrow below indicates the game is listening for a command.")
        command = input("> ").lower()

    def start(self):
        """Entrypoint for the game. Starts the game loop"""

        # Main game loop
        while self.alive:
            # print status details
            linked_caves = self.map.linked_caves(self.current_cave)
            # get numbers of each cave linked to this one
            linked_caves_str = ", ".join(map(lambda cave: f"[{cave.num}]",linked_caves))
            print("\n")
            print(f"[{self.current_cave.num}]: {self.current_cave.name}")
            print("---*---*---")
            print(f"{self.current_cave.description}")
            print(f"This cave is linked to caves {linked_caves_str}")
            print("---*---*---")
            
            command = input("> ").lower()

            try:
                # move to cave if cave number is inputted
                cmd_cave_num = int(command)
                if cmd_cave_num not in map(lambda cave: cave.num, linked_caves):
                    print("You cannot go that way!")
                    continue
            except:
                pass # do nothing

            # handle other commands
            if command.startswith(""):
                pass # TODO: handle other commands