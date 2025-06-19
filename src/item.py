class Item:
    """Represents an item in the game
    """

    def __init__(self, name, emoji, description):
        self.name = name
        self.emoji = emoji
        self.description = description

    def get_display():
        """Return the name of the item along with its representative emoji"""
        return f"{self.emoji} {self.name}"

    def get_name():
        """Returns the item's name"""
        return self.name

    def get_description():
        """Return the item's description"""
        return self.description