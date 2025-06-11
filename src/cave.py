class Cave:
    """Represents a single room in the game the player may enter. Must have a unique number assigned to it

    May be composed of Characters and Items
    """
    def __init__(self, num, name, description, map):
        self.num = num
        self.name = name
        self.description = description
        self.map = map

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

    # Item handling
    def get_items(self):
        return self.items
    
    def add_item(self, new_item):
        self.items.add(new_item)

    def remove_item(self, item):
        self.items.remove(item)

    def clear_items(self):
        """Remove all items from this cave"""
        self.items.clear()

    # character handling
    def add_character(self, new_character):
        self.characters.add(new_character)

    def remove_character(self, character):
        self.characters.remove(character)
