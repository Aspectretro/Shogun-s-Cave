from map import Map
from item import Item
from cave import Cave
from character import Enemy
from character import Friendly
import random as r

class Game:
    """Class that manages all aspects of a currently running session, including the player 

    All other classes are managed by an instance of this class
    """
    def __init__(self):
        self.alive = True

        # Generate map
        self.map = Map(self)
        self.map.generate()

        self.current_cave = self.map.starting_cave # initially the player begins in the starting cave
    
    def tutorial(self):
        # TODO: tutorial
        """Start the tutorial for the game. Does not begin the main game loop"""

        print("\n")
        print("Welcome to [game name]! This is the tutorial and will show you how the game works.")
        print("In this game, you will be dropped into a series of unknown caverns, and your goal is to survive and find a way out.")
        print("Throughout your adventure inside this deep, dark world, you will encounter monsters, and potential friendlies.")
        print("Here is a list of commands you can use when you are within the game:")
        print("Move: type in a number of the linked caves to move.")
        print("Fight: fight the appeared character/enemy with an item that you possess.")
        print("Pat: pat the appeared character/enemy")
        print("Shop: open up the item purchase menu when in a shop") # TODO: create corresponding commands
        print("If you are already familiar with the game, enter q to skip.")
        print("\n")

        print("This arrow below indicates the game is listening for a command.")
        command = input("> ").lower()

        # setters
    def set_cave(self, cave):
        """Set the current cave the player is in.

        Does nothing if the player is no longer alive
        """
        if not self.alive:
            return
        
        self.current_cave = cave

    def start(self):
        """Entrypoint for the game. Starts the game loop"""

        # Main game loop
        while self.alive:
            # print status details
            linked_caves = self.map.linked_caves(self.current_cave)
            # get numbers of each cave linked to this one
            linked_caves_str = ", ".join(map(lambda cave: f"[{cave.num}]",linked_caves))
            print("\n")
            print(f"[{self.current_cave.num}]: {self.current_cave.name}")
            print("---*---*---")
            print(f"{self.current_cave.description}")
            print(f"This cave is linked to caves {linked_caves_str}")
            print("---*---*---")
            
            command = input("> ").lower()

            try:
                # move to cave if cave number is inputted
                cmd_cave_num = int(command)
                if cmd_cave_num not in map(lambda cave: cave.num, linked_caves):
                    print("You cannot go that way!")
                    continue
            except:
                pass # do nothing
            # handle other commands
            if command.startswith(""):
                pass # TODO: handle other commands

            inhabitance = self.current_cave.get_characters()
            if command == "fight":
                """When encountering a ninja, instead of fighting, you get teleported to a random location"""
                if bool(inhabitance) == True:
                    print("Who would you want to fight?")
                    for items in inhabitance:
                        print(items)
                    fight_with = input("> ")
                    try:
                        # begin fight if the character chosen is within the set
                        if fight_with in inhabitance:
                            if isinstance(fight_with, Enemy): # TODO: method of detecting the correct class of fight_with
                                print(f"What item will you use to defend yourself from {fight_with}")
                                fight_item = input("> ")
                                if fight_item == inhabitance.weakness():
                                    print("Sucess")
                                else:
                                    print("You died")
                                    self.alive = False # you are dead, break the loop
                            elif isinstance(fight_with, Friendly):
                                pass
                    except:
                        pass

                else:
                    print("There are no one here to fight with.")

            if command == "pat":
                pass

            if command == "help": # TODO: display tutorial page
                print("Here is a list of commands available:")
                print("Move: type in a number of the linked caves to move.")
                print("Fight: fight the appeared character/enemy with an item that you possess.")
                print("Pat: pat the appeared character/enemy")
                print("Shop: open up the item purchase menu when in a shop")