class Character:
    """Represents a non-player character with an optional voice line
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description

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

    def set_conversation(self, new_conversation):
        """Sets this character's voice line, overriding any existing voice line"""
        self.conversation = new_conversation

    def get_conversation(self):
        return self.conversation


class Enemy(Character):
    """Represents a character that acts as an enemy to the player
    """

    def __init__(self, name, description):
        super().__init__(name, description)  # initialise superclass

        # Optional attributes
        self.weakness = None

    # Setters and getters
    def set_weakness(self, weakness):
        """Sets this enemy's weakness, overriding any existing value. Pass None for no weakness"""
        self.weakness = weakness

    def get_weakness(self):
        return self.weakness

    def fight(self, item):
        pass # TODO: Stub implementation
