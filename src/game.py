from map import MapGraph
from item import Item
from character import Enemy
from character import Friendly
import random as r


class Game:
    """Class that manages all aspects of a currently running session, including the player

    All other classes are managed by an instance of this class
    """

    """
    TODO list:
    - Boss characterization (add boss fight. Ensure it is different from normal fights with other hostiles)
    - Egg impl (add easter egg location)
    - Shop system fix & impl (fix setting detection)
    - Item impl (add item, bag)
    - Pits impl (add method & attributes for pits)
    """

    def __init__(self):
        self.alive = True
        self.items = set()  # the player's items - they may only have one of each item
        self.purse = 20 # currency: the player starts with 20

        # Generate map
        self.map = MapGraph.generate(self)

        # initially the player begins in the starting cave
        self.current_cave = self.map.get_cave(1)

        # Whether the status message needs to be printed again
        self.status_dirty = True

    # TODO tutorial menu
    def tutorial(self):
        """Start the tutorial for the game. Does not begin the main game loop"""

        print("\n")
        print(
            "Welcome to Shogunate's Caverns! This is the tutorial and will show you how the game works.")
        print("In this game, you will be dropped into a series of unknown caverns, and your goal is to survive and find a way out.")
        print("Throughout your adventure inside this deep, dark world, you will encounter various enemies and maybe even some allies.")
        print("---") 
        print("To interact with your environment you can issue commands to the game")
        print("The following commands are available:")
        print("  fight:   Start a fight with any character in the current cave. You need an item to fight them with!")
        print("  pat:     Path any character in the current cave.")
        print("  shop:    Open up the shop, if the current cave allows it")
        print("  refresh: Refresh the game window to clear up clutter")
        print("")
        print("  Any number will be treated as a command to move to that cave")
        print("  To issue a command, type the command's name and press Enter")
        print("")
        print("If you are already familiar with the game, type q and then press Enter to skip..")
        print("\n")
        print("This arrow below indicates the game is listening for some input.")
        command = input("> ").lower()

        if command == "q":
            return # skip this whole tutorial section

        # setters
    def set_cave(self, cave_num):
        """Set the current cave the player is in by number.

        Does nothing if the player is no longer alive
        """
        if not self.alive:
            return

        if cave_num == self.current_cave.num:
            return  # do not change caves if they are the same cave

        self.current_cave = self.map.get_cave(cave_num)
        # set dirty
        self.status_dirty = True

    def start(self):
        """Entrypoint for the game. Starts the game loop"""

        # Main game loop
        while self.alive:
            # print status details
            characters = self.current_cave.get_characters()
            linked_caves = self.map.linked_caves(self.current_cave)
            # get numbers of each cave linked to this one
            linked_caves_str = ", ".join(
                map(lambda cave: f"[{cave.num}]", linked_caves))

            # status message, print if dirty
            if self.status_dirty:
                # magic numbers: ANSI "clear screen" characters
                print("\033[H\033[J", end="")
                print("---*---*---")
                print(f"[{self.current_cave.num}]: {self.current_cave.name}")
                print("-----------")
                print(f"{self.current_cave.description}")
                print(f"This cave is linked to caves {linked_caves_str}")
                print("-----------")
                if len(characters) > 0:
                    print(f"You aren't alone in here! You see:")
                    for character in characters:
                        print(f"  A {character.name}: {character.description}")
                else:
                    print(f"It seems like there is no one else here")
                print("---*---*---")
                # end status message
                # set status to clean (dirty = False) once printed
                self.status_dirty = False

            # get command from user regardless of status dirty
            command = input("> ").lower()

            try:
                # move to cave if cave number is inputted
                cmd_cave_num = int(command)

                if cmd_cave_num == self.current_cave.num:
                    print("You're already at that cave!")
                    continue

                # check if the cave is valid
                if not self.map.check_link(self.current_cave.num, cmd_cave_num):
                    print("You can't go that way!")
                    continue

                # if it is, set the players cave to there
                self.set_cave(cmd_cave_num)
            except:
                pass  # do nothing

            # Shop item list
            shop_menu = {'Torch': 10,
                         'Sword': 20,
                         'Axe': 15}
            

            # handle other commands
            match command:
                case "refresh":
                    self.status_dirty = True
                case "clear":
                    self.status_dirty = True
                case "fight":
                    if len(self.items) <= 0:
                        print("You don't have any items to fight with...")
                        continue

                    if len(characters) > 0:
                        print(
                            "Who do you want to fight? Input the number in brackets next to the character you would like to battle with.")
                        for (i, character) in enumerate(characters):
                            # print index + 1 next to characters
                            # stating a number will be how the user selects which character to fight
                            print(f"[{i + 1}]: {character.name}")

                        try:
                            fight_with_num = int(input("> "))

                            if fight_with_num > len(character) or fight_with_num <= 0:
                                print(
                                    "That isn't a valid character in this cave!")
                                continue

                            # subtract 1 to balance out i + 1 earlier
                            selected_character = character[fight_with_num - 1]

                            # do not permit players to fight Friendly characters
                            if isinstance(selected_character, Friendly):
                                print(
                                    f"{selected_character} is a friend, not a foe! You can't fight them!")
                                continue

                            # ask player for an item to fight with
                            print(
                                "Please select one item you want to use in battle. Input the number in brackets next to the item you would like to use.")
                            for (i, item) in enumerate(self.items):
                                # print index + 1 next to player's items
                                print(f"[{i + 1}]: {item.name}")

                            fight_item_num = int(input("> "))
                            if fight_item_num > len(self.items) or fight_item_num <= 0:
                                print("That isn't an item you have!")
                                continue

                            selected_character.fight(
                                self.items[fight_item_num - 1])
                        except ValueError:
                            print("That isn't a valid number!")
                        except:
                            pass

                    else:
                        print("There are no one here to fight with.")
                case "pat":
                    if len(characters) > 0:
                        print("Who will you pat?")
                    # TODO: change the variable that handles the list of characters within the instance.
                    for items in inhabitance:
                        print(items)
                    pat_char = input("> ")
                    try:
                        if pat_char in inhabitance:
                            if isinstance(pat_char, Friendly):
                                print(f'You have patted {pat_char}')
                        elif isinstance(pat_char, Enemy):
                            print("Ain't no way you are thinking of doing that...")
                        else:
                            print(f'{pat_char} is not here with you')
                    except:
                        pass
                case "help":
                    print("Here is a list of commands available:")
                    print("Move: type in a number of the linked caves to move.")
                    print("Fight: fight the appeared character/enemy with an item that you possess.")
                    print("Pat: pat the appeared character/enemy")
                    print("Shop: open up the item purchase menu when in a shop")

                case "shop":
                    if self.current_cave.name == "Shop":
                        # Open shop menu
                        print("This is the shop. A place of safety and where transactions are done.")
                        print("If you are purchasing an item, type in the name of the item in the product list.")
                        print("If you are not going to purchase anything, type in leave and exit the menu.")
                        n = 1
                        for item in shop_menu:
                            print(f'{n}. {item}')
                            n += 1
                        purchase = input("> ")
                        cost = shop_menu[purchase]
                        if purchase in shop_menu:
                            if self.purse < cost:
                                print("You don't have enough money to purchase this item.")
                            else:
                                self.purse -= cost
                                print(f'You have successfully purchased {purchase} from the shop.')
                                shop_menu.pop(purchase) # .pop methods removes the item and its corresponding value from the dictionary permanently
                                self.items.add(purchase) # add the purchased item into the inventory
                                if purchase == "leave":
                                    self.status_dirty = True
                        
                        if purchase == "leave":
                            self.status_dirty = True
                
                case "items":
                    for items in self.items:
                        print(self.items)
                    if len(self.items) == 0:
                        print("Empty pockets!")