class Item:
    """Represents an item in the game
    """

    def __init__(self, name, emoji, description, cost, damage=0):
        self.name = name
        self.emoji = emoji
        self.description = description
        self.cost = cost
        self.damage = damage # damage the item does

    def get_display(self):
        """Return the name of the item along with its representative emoji"""
        return f"{self.emoji} {self.name}"

    def get_name(self):
        """Returns the item's name"""
        return self.name

    def get_description(self):
        """Return the item's description"""
        return self.description
    
    def get_cost(self):
        """Return this item's cost"""
        return self.cost

    def get_damage(self):
        """Return this item's damage"""
        return self.damage 

    def set_damage(self, new_damage):
        """Set this item's damage"""
        self.damage = new_damage