class Item:
    """Represents an item in the game
    """

    def __init__(self, name, emoji, description, cost):
        self.name = name
        self.emoji = emoji
        self.description = description
        self.cost = cost

    def get_display():
        """Return the name of the item along with its representative emoji"""
        return f"{self.emoji} {self.name}"

    def get_name():
        """Returns the item's name"""
        return self.name

    def get_description():
        """Return the item's description"""
        return self.description
    
    def get_cost():
        """Return this item's cost"""
        return self.cost