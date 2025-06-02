class Cave:
    """Represents a single room in the game the player may enter.

    May be composed of Characters and Items
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description