from cave import Cave
from character import Ninja
import random

class Map:
    """A class that represents the map of caves in the game
    """
    
    def __init__(self, game):
        self.starting_cave = None
        self.map = {}
        self.game = game

    def generate(self):
        """Fill in the map with new caves, overwriting the current map"""
        # TODO: names and descriptions
        cave1 = Cave(1, "Cave", "A small cave underground. No light seeps through although there are cracks in the ceiling", self)
        cave2 = Cave(2, "Shop", "A nice and cozy room with a counter, some products.", self)
        cave3 = Cave(3, "Pit", "Deep, dark, bottomless, hole. Take care with your footing", self)
        cave4 = Cave(4, "Dungeon", "Echoes of unseen horrors lurking beyond the flickering torchlight.", self)
        cave5 = Cave(5, "Dungeon", "A large room with some equipments and some metallic racks", self)
        cave6 = Cave(6, "Lava Tube", "Just a long tunnel with a sense of cold and dreadfulness", self)
        cave7 = Cave(7, "Grotto", "A cathedral of stone where time pools in the hush of dripping stalactites.", self)
        cave8 = Cave(8, "Shop", "A nice and cozy room with a counter, some products.", self)
        cave9 = Cave(9, "Pit", "Deep, dark, bottomless, hole. Take care with your footing", self)
        cave10 = Cave(10, "Cave", "A small cave underground. A glimpse of light and some gentle gusts of air seeps through the gaps between the rocks.", self)
        cave11 = Cave(11, "Room", "An enormous space with a throne like chair in the middle.", self)
        cave12 = Cave(12, "Grotto", "A shadowed sanctuary where time drips like water from the jagged limestone.", self)

        ninja = Ninja(cave4)
        cave4.add_character(ninja)

        self.map = {
            cave1: [cave2, cave3, cave4, cave5],
            cave2: [cave1, cave6, cave9],
            cave3: [cave1, cave6, cave7],
            cave4: [cave1, cave9, cave8],
            cave5: [cave1, cave7, cave8],
            cave6: [cave2, cave3, cave12],
            cave7: [cave3, cave5, cave11, cave12],
            cave8: [cave4, cave5, cave10, cave11],
            cave9: [cave2, cave4, cave10],
            cave10: [cave8, cave9],
            cave11: [cave7, cave8],
            cave12: [cave6, cave7]
        }

        # Set starting cave
        self.starting_cave = cave1

    def linked_caves(self, cave):
        """Return a list of linked caves to the one provided"""
        return self.map[cave]

    def rand_cave(self):
        """Return a random cave in the list of caves"""
        return random.choice(self.map)

    def move(self, dir):
        for dir in self.linked_caves():
            cave = self.linked_caves[dir] # TODO: iterate over caves, check for backlinks