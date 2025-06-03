from cave import Cave

class Map:
    """A class that represents the map of caves in the game
    """
    
    def __init__(self):
        self.starting_cave = None
        self.map = {}

    def generate(self):
        """Fill in the map with new caves, overwriting the current map"""
        # TODO: names and descriptions
        cave1 = Cave(1, "Cave", "A small cave underground. A little light seeps in from a crack in the ceiling")
        cave2 = Cave(2, "Grotto", "A cramped and damp recess. Maybe it would be a great place to hide...")
        cave3 = Cave(3, "Cavern", "A large, spacious cavern")

        self.map = {
            cave1: cave2,
            cave2: cave3,
            cave3: cave1
        }

        # Set starting cave
        self.starting_cave = cave1

    def linked_caves(self, dir):
        """Return a list of linked caves to the one provided"""
        link = self.map[dir]

    def move(self, dir):
        for dir in self.linked_caves():
            cave = self.linked_caves[dir]
            print(f'The') # TODO: iterate over caves, check for backlinks