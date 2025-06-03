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

    def start(self):
        """Entrypoint for the game. Starts the game loop"""
        while self.alive:
            pass