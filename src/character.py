import display

class Character:
    """Represents a non-player character with an optional voice line
    """

    def __init__(self, name, description, cave):
        self.name = name
        self.description = description
        self.cave = cave

        # Optional attributes
        self.conversation = None

    # Setters and getters
    def set_description(self, new_desc):
        """Sets a new description for this character, if the provided description is not None"""
        if new_desc is not None:
            self.description = new_desc

    def get_description(self):
        return self.description

    def set_name(self, new_name):
        """Sets a new name for this character, if the provided name is not None"""
        if new_name is not None:
            self.name = new_name

    def get_name(self):
        return self.name

    def set_conversation(self, new_conv):
        """Sets this character's voice line, overriding any existing voice line"""
        self.conversation = new_conv

    def get_conversation(self):
        return self.conversation


class Enemy(Character):
    """Represents a character that acts as an enemy to the player
    """

    def __init__(self, name, description, health, cave):
        super().__init__(name, description, cave)  # initialise superclass

        self.health = health
        self.total_health = health

        # Optional attributes
        self.weakness_item_name = None # defeats the enemy right away
        self.drop = None # item this enemy drops on defeat

    # Setters and getters
    def set_weakness(self, weakness):
        """Sets this enemy's weakness, overriding any existing value. Pass None for no weakness"""
        self.weakness_item_name = weakness

    def get_weakness(self):
        return self.weakness_item_name

    def set_drop(self, item):
        """Set this enemy's drop item"""
        self.drop = item

    def get_drop(self):
        """Get the item this enemy drops"""
        return self.drop

    def get_health(self):
        """Get the health of this enemy"""
        return self.health

    def get_total_health(self):
        """Get the initial total health of this enemy"""
        return self.total_health

    def fight(self, item):
        """Fight sequence for this enemy"""
        if item.damage >= self.health:
            # enemy defeated!
            self.health = 0
            return True
        self.health -= item.damage # apply damage to enemy
        if item.name == self.weakness_item_name:
            # enemy defeated!
            return True
        else:
            # damaged enemy but not defeated
            return False
        

class Boss(Enemy):
    """Final enemy of the game. After killing it, player is allowed to exit or continue to travel within the caves
    
       On Boss kill, the boss will drop currencies that will allow the player to purchase the obsidian key from the shop
       in order to unlock the hidden ending which is located in shop 10.
    """
    def __init__(self, name, description, cave):
        super().__init__(name, description, 1_000_000, cave)
    
    def set_weakness(self, weakness):
        return super().set_weakness(weakness)
    
    def get_weakness(self):
        return super().get_weakness()
    
    def fight(self, item):
        # Boss fight sequence
        display.speech_box("You dare challenge me, little fool?", self.name)
        # You can only defeat a boss with its weakness
        if item.name != self.weakness_item_name:
            return False

class Ninja(Enemy):
    """A special type of enemy that can kidnap the player and transport them to a random cave"""

    def __init__(self, cave):
        super().__init__("Ninja", "A black shadowy figure that looks ready to strike", 1, cave) # health doesn't matter, you can't fight ninjas

    def fight(self, item):
        """If a player chooses to fight with a ninja they will kidnap them"""
        # kidnapping procedure
        display.alert_box(f"You try to fight the ninja with your {item.name}, but they quickly drop a smoke bomb!")
        random_cave = self.cave.map.random_cave()
        # send player to random cave
        self.cave.map.game.set_cave(random_cave.num)
        display.alert_box(f"The smoke clears and you're suddenly in a different cave!")


class Friendly(Character):
    def __init__(self, name, description, cave):
        super().__init__(name, description, cave) # initialise super class
        self.conversation = None