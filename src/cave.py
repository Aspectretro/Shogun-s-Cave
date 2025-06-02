class Cave:
    """Represents a single room in the game the player may enter.

    May be composed of Characters and Items
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description

        # Optional attributes
        self.characters = set() # set to ensure a character cannot appear twice in a room
        self.items = set() # similarly, an item should only appear once in a room

    # Setters and getters    
    def set_description(self, new_desc):
        """Sets a new description for this cave, if the provided description is not None"""
        if new_desc is not None:
            self.description = new_desc
    def get_description(self):
        return self.description

    def set_name(self, new_name):
        """Sets a new name for this cave, if the provided name is not None"""
        if new_name is not None:
            self.name = new_name
    def get_name(self):
        return self.name

    # TODO: multi-character and item handling
