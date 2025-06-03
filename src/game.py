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

    def start(self):
        """Entrypoint for the game. Starts the game loop"""

        # Main game loop
        while self.alive:
            # print status details
            print("\n")
            print(f"[{self.current_cave.num}]: {self.current_cave.name}")
            print("---*---*---")
            print(f"{self.current_cave.description}")
            print(f"")
            print("---*---*---")
            
            command = input("> ").lower()