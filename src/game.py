from map import MapGraph
from item import Item
from character import Enemy
from character import Friendly
from cave import Cave, Shop
import random as r
import display
import parsing
import cmd
import sys
import tty
import termios


# TODO: custom help cmd
class Game(cmd.Cmd):
    prompt = "> "
    ruler = "-"

    nohelp = "Command '%s' not found!"

    def __init__(self):
        super().__init__(None)  # override complete key (no completion)

        self.alive = True
        # Whether the status message needs to be printed again
        self.__dirty = True
        # Generate map
        self.map = MapGraph.generate(self)
        # initially the player begins in the starting cave
        self.current_cave = self.map.get_cave(1)

        self.purse = 20  # the player's coins
        self.items = []

    def tutorial(self):
        pass

    def start(self):
        self.cmdloop()

    def __set_cave(self, cave_num):
        """Set the current cave by number

        Does nothing if the player is not alive
        """

        if not self.alive:
            return

        if cave_num == self.current_cave.num:
            return  # don't change caves if they are in the same cave already

        self.current_cave = self.map.get_cave(cave_num)
        self.__set_dirty()

    def __set_dirty(self):
        """Set status message to refresh on the next loop iteration"""
        self.__dirty = True

    def __unset_dirty(self):
        self.__dirty = False

    # ---
    # Commands
    # ---

    def do_refresh(self, arg):
        """Refresh the game window to clear up clutter"""

        self.__set_dirty()

    def do_quit(self, arg):
        """Quit and close the game"""
        confirmation = display.confirm("Are you sure you would like to quit?")
        if confirmation:
            print("\nThank you for playing Shogunate's Caverns!")
            return True

        print("OK, not quitting.")

    def do_move(self, arg):
        """Go to a cave linked to the one you're currently in"""

        # check arg has actual characters
        if not len(arg):
            print(
                f"No cave number specified! Please try again, specifying a cave number!")
            display.print_hint("If you want to go to cave 2, type 'move 2'")
            return

        input_int = parsing.parse_int(arg)

        if input_int is None:
            print(f"'{arg}' was not a valid cave!")
            display.print_hint("If you want to go to cave 2, type 'move 2'")
            return

        if input_int == self.current_cave.num:
            return print(f"You're already at cave {display.bold(input_int)}!")

        # Check cave accessibility
        if not self.map.check_link(self.current_cave.num, input_int):
            return print("You can't go that way!")

        # Set players cave
        self.__set_cave(input_int)

    def do_fight(self, arg):
        """Start a fight with a character"""
        characters = self.current_cave.characters
        if not len(characters):
            print("There is no one to fight here.")
            return

        if not len(self.items):
            print("You have no items to fight with!")
            display.print_hint(
                "Buy items in Shops, or find them in certain caves")
            return

        print("Select a character to fight by inputting the number in brackets next to their name!")

        for (i, character) in enumerate(characters):
            # print i + 1 next to characters' names
            print(f"├╴ [{i + 1}]: {display.underline(character.name)}")
        print(f"╰╴ [{len(characters) + 1}]: Cancel fight")

        fight_with_int = display.prompt("Please select a character", 1, "int",
                                        lambda num: "That isn't a valid option" if num > len(characters) + 1 or num <= 0 else True)

        if fight_with_int == len(characters) + 1:
            # cancel fight option
            print("Fight cancelled!")
            return

        # subtract 1 to balance out the i + 1 earlier
        selected_character = characters[fight_with_int - 1]

        # do not permit players to fight friendly characters
        if isinstance(selected_character, Friendly):
            print(
                f"{selected_character.name} is a friend, not a foe! You can't fight them")
            return

        print("Please select one item you want to use in battle.")
        for (i, item) in enumerate(self.items):
            # print i + 1 next to items' names
            print(f"├╴ [{i + 1}]: {item.name}")
        print(f"╰╴ [{len(self.items) + 1}]: Cancel fight")

        fight_item_int = display.prompt("Please select an item", 1, "int", lambda num: "That isn't an item you have!" if num > len(
            self.items) + 1 or num <= 0 else True)

        if fight_item_int == len(self.items) + 1:
            print("Fight cancelled")
            return

        selected_item = self.items[fight_item_int - 1]

        # FEAT: Fight sequence

    def do_shop(self, arg):
        """Open up the shop in this cave, if there is one"""
        if not isinstance(self.current_cave, Shop):
            print("There isn't a shop here!")
            display.print_hint(
                "You can only open the shop in caves that have a shop in them!")
            return

        print("Welcome to the shop, a place of safety where transactions are done.")
        print("Please select the item you wish to purchase by entering its number in brackets!")

        print(f"You have {display.colour(220, f"${self.purse}")
                          } | The following items are for sale:")

        for (i, item) in enumerate(self.current_cave.for_sale):
            cost_display = f"${item.cost}"
            # if the player cannot afford the item, colour it red
            if item.cost > self.purse:
                cost_display = display.colour(160, cost_display)
            else:  # else make it green
                cost_display = display.colour(34, cost_display)
            print(f"├╴ [{i + 1}] {item.name} ({cost_display})")
        print(
            f"╰╴ [{len(self.current_cave.for_sale) + 1}] Leave without buying anything")

        item_int = display.prompt("Please select an item", 1, "int", lambda num: "That isn't a valid item!" if num > (len(
            self.current_cave.for_sale) + 1) or num <= 0 else True)

        if item_int == len(self.current_cave.for_sale) + 1:
            # exit shop
            print("Leaving the shop!")
            return

    # ---
    # Overridden methods
    # ---

    def emptyline(self):
        pass  # no-op

    def default(self, line):
        print("Command not found. Please try again!")

    def cmdloop(self, intro=None):
        self.preloop()

        # Reimplemented from stdlib, but with cave-related status messages

        try:
            # whether to stop the loop
            stop = None
            while not stop:
                # if dirty, unset dirty and print status message
                if self.__dirty:
                    self.__unset_dirty()

                    characters = self.current_cave.get_characters()
                    linked_caves = self.map.linked_caves(self.current_cave)
                    # get numbers of each cave linked to this one
                    linked_caves_str = ", ".join(
                        map(lambda cave: f"[{cave.num}]", linked_caves))

                    # begin status message
                    display.clear()
                    print("---*---*---")
                    print(
                        f"You are in cave [{display.bold(self.current_cave.num)}]: A {self.current_cave.name}")
                    print("-----------")
                    print(f"{self.current_cave.description}")
                    print(f"This cave is linked to caves {linked_caves_str}")
                    if isinstance(self.current_cave, Shop):
                        print(
                            "🛍️  There is a shop here! Use the 'shop' command to check it out!")
                    print("-----------")
                    if len(characters) > 0:
                        print(f"You aren't alone in here! You see:")
                        for character in characters:
                            print(
                                f"  A {display.underline(character.name)}: {character.description}")
                    else:
                        print(f"It seems like there is no one else here")
                    print("---*---*---")
                    # end status message

                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    self.stdout.write(self.prompt)
                    self.stdout.flush()
                    # Construct a line from reading each character from stdin
                    line = ""
                    cursor = 0  # position of typing cursor
                    # set tty to raw to disable buffering
                    normal_tty = termios.tcgetattr(self.stdin)
                    tty.setraw(self.stdin)
                    while True:
                        char = self.stdin.read(1)  # read one character
                        char_code = ord(char)

                        # user hit enter key
                        if char == '\r' or char == '\n':
                            break  # exit

                        # backspace key
                        if char_code == 127:
                            # delete one character
                            line = line[:cursor - 1] + line[cursor:]
                            cursor = max(cursor - 1, 0)

                        # special key handling (ANSI '[' sequence)
                        # 3 character sequences starting with [
                        if char_code == 27:
                            next1, next2 = ord(self.stdin.read(1)), ord(
                                self.stdin.read(1))

                            if next1 == 91:

                                if next2 in [50, 53, 54]: # ins, pgup, pgdn
                                    next3 = self.stdin.read(1)
                                    # no op, just swallow "~" sign

                                if next2 == 51:  # delete key
                                    next3 = self.stdin.read(1)
                                    if next3 == "~":
                                        line = line[:cursor] + \
                                            line[cursor + 1:]

                                # arrow keys
                                if next2 == 68:  # left
                                    cursor = max(cursor - 1, 0)
                                if next2 == 67:  # right
                                    cursor = min(
                                        len(line), cursor + 1)

                        # if character is regular ASCII character
                        # add to line buffer and +1 to index
                        if 32 <= char_code < 127:
                            line = line[:cursor] + char + line[cursor:]
                            cursor += 1

                        # print buffered line
                        # send cursor to line start
                        self.stdout.write("\033[1000D")
                        self.stdout.write("\033[0K")  # erase line
                        self.stdout.write(self.prompt + line)  # write line
                        # send cursor to line start
                        self.stdout.write("\033[1000D")
                        # set cursor pos
                        self.stdout.write(f"\033[{cursor + len(self.prompt)}C")
                        self.stdout.flush()  # flush to terminal
                    # loop done, reset tty to normal
                    termios.tcsetattr(
                        self.stdin, termios.TCSADRAIN, normal_tty)
                    print("")

                    if not len(line):
                        line = 'EOF'
                    else:
                        line = line.strip()

                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)

            self.postloop()
        finally:
            pass


# class Game:
#     """Class that manages all aspects of a currently running session, including the player

#     All other classes are managed by an instance of this class
#     """

#     """
#     TODO list:
#     - Boss characterization (add boss fight. Ensure it is different from normal fights with other hostiles)
#     - Egg impl (add easter egg location)
#     - Shop system fix & impl (fix setting detection)
#     - Item impl (add item, bag)
#     - Pits impl (add method & attributes for pits)
#     """

#     def __init__(self):
#         self.alive = True
#         self.items = set()  # the player's items - they may only have one of each item
#         self.purse = 20  # currency: the player starts with 20

#         # Generate map
#         self.map = MapGraph.generate(self)

#         # initially the player begins in the starting cave
#         self.current_cave = self.map.get_cave(1)

#         # Whether the status message needs to be printed again
#         self.status_dirty = True

#     # TODO tutorial menu
#     def tutorial(self):
#         """Start the tutorial for the game. Does not begin the main game loop"""

#         print("\n")
#         print(
#             "Welcome to Shogunate's Caverns! This is the tutorial and will show you how the game works.")
#         print("In this game, you will be dropped into a series of unknown caverns, and your goal is to survive and find a way out.")
#         print("Throughout your adventure inside this deep, dark world, you will encounter various enemies and maybe even some allies.")
#         print("---")
#         print("To interact with your environment you can issue commands to the game")
#         print("The following commands are available:")
#         print("  fight:   Start a fight with any character in the current cave. You need an item to fight them with!")
#         print("  pat:     Pat any character in the current cave.")
#         print("  shop:    Open up the shop, if the current cave allows it")
#         print("  refresh: Refresh the game window to clear up clutter")
#         print("")
#         print("  Any number will be treated as a command to move to that cave")
#         print("  To issue a command, type the command's name and press Enter")
#         print("")
#         print("If you are already familiar with the game, type q and then press Enter to skip..")
#         print("\n")
#         print("This arrow below indicates the game is listening for some input.")
#         command = input("> ").lower()

#         if command == "q":
#             return  # skip this whole tutorial section

#         # setters
#     def set_cave(self, cave_num):
#         """Set the current cave the player is in by number.

#         Does nothing if the player is no longer alive
#         """
#         if not self.alive:
#             return

#         if cave_num == self.current_cave.num:
#             return  # do not change caves if they are the same cave

#         self.current_cave = self.map.get_cave(cave_num)
#         # set dirty
#         self.status_dirty = True

#     def start(self):
#         """Entrypoint for the game. Starts the game loop"""

#         # Main game loop
#         while self.alive:
#             # print status details
#             characters = self.current_cave.get_characters()
#             linked_caves = self.map.linked_caves(self.current_cave)
#             # get numbers of each cave linked to this one
#             linked_caves_str = ", ".join(
#                 map(lambda cave: f"[{cave.num}]", linked_caves))

#             # status message, print if dirty
#             if self.status_dirty:
#                 display.clear()
#                 print("---*---*---")
#                 print(f"[{self.current_cave.num}]: {self.current_cave.name}")
#                 print("-----------")
#                 print(f"{self.current_cave.description}")
#                 print(f"This cave is linked to caves {linked_caves_str}")
#                 print("-----------")
#                 if len(characters) > 0:
#                     print(f"You aren't alone in here! You see:")
#                     for character in characters:
#                         print(f"  A {character.name}: {character.description}")
#                 else:
#                     print(f"It seems like there is no one else here")
#                 print("---*---*---")
#                 # end status message
#                 # set status to clean (dirty = False) once printed
#                 self.status_dirty = False

#             # get command from user regardless of status dirty
#             command = input("> ").lower()

#             try:
#                 # move to cave if cave number is inputted
#                 cmd_cave_num = int(command)

#                 if cmd_cave_num == self.current_cave.num:
#                     print("You're already at that cave!")
#                     continue

#                 # check if the cave is valid
#                 if not self.map.check_link(self.current_cave.num, cmd_cave_num):
#                     print("You can't go that way!")
#                     continue

#                 # if it is, set the players cave to there
#                 self.set_cave(cmd_cave_num)
#             except:
#                 pass  # do nothing

#             # Shop item list
#             shop_menu = {'Torch': 10,
#                          'Sword': 20,
#                          'Axe': 15}

#             # handle other commands
#             match command:
#                 case "refresh":
#                     self.status_dirty = True
#                 case "clear":
#                     self.status_dirty = True
#                 case "fight":
#                     if len(self.items) <= 0:
#                         print("You don't have any items to fight with...")
#                         continue

#                     if len(characters) > 0:
#                         print(
#                             "Who do you want to fight? Input the number in brackets next to the character you would like to battle with.")
#                         for (i, character) in enumerate(characters):
#                             # print index + 1 next to characters
#                             # stating a number will be how the user selects which character to fight
#                             print(f"[{i + 1}]: {character.name}")

#                         try:
#                             fight_with_num = display.prompt(
#                                 "Please select a character", 1, "int", lambda num: "That isn't a valid character in this cave!" if num > len(characters) or num <= 0 else True)

#                             # subtract 1 to balance out i + 1 earlier
#                             selected_character = characters[fight_with_num - 1]

#                             # do not permit players to fight Friendly characters
#                             if isinstance(selected_character, Friendly):
#                                 print(
#                                     f"{selected_character} is a friend, not a foe! You can't fight them!")
#                                 continue

#                             print(f"Fighting the {selected_character.name}!")

#                             # ask player for an item to fight with
#                             print(
#                                 "Please select one item you want to use in battle. Input the number in brackets next to the item you would like to use.")
#                             for (i, item) in enumerate(self.items):
#                                 # print index + 1 next to player's items
#                                 print(f"[{i + 1}]: {item.name}")

#                             fight_item_num = int(input("> "))
#                             if fight_item_num > len(self.items) or fight_item_num <= 0:
#                                 print("That isn't an item you have!")
#                                 continue

#                             selected_character.fight(
#                                 self.items[fight_item_num - 1])
#                         except ValueError:
#                             print("That isn't a valid number!")
#                         # except:
#                         #     # FIXME: error message/breakpoint check here
#                         #     pass

#                     else:
#                         print("There are no one here to fight with.")
#                 case "pat":
#                     if len(characters) > 0:
#                         print("Who will you pat?")
#                     # TODO: change the variable that handles the list of characters within the instance.
#                     for items in inhabitance:
#                         print(items)
#                     pat_char = input("> ")
#                     try:
#                         if pat_char in inhabitance:
#                             if isinstance(pat_char, Friendly):
#                                 print(f'You have patted {pat_char}')
#                         elif isinstance(pat_char, Enemy):
#                             print("Ain't no way you are thinking of doing that...")
#                         else:
#                             print(f'{pat_char} is not here with you')
#                     except:
#                         pass
#                 case "help":
#                     print("Here is a list of commands available:")
#                     print("Move: type in a number of the linked caves to move.")
#                     print(
#                         "Fight: fight the appeared character/enemy with an item that you possess.")
#                     print("Pat: pat the appeared character/enemy")
#                     print("Shop: open up the item purchase menu when in a shop")

#                 case "shop":
#                     if isinstance(self.current_cave, Shop):
#                         print(
#                             "Welcome to the shop, a place of safety where transactions can be done")
#                         print(
#                             "If you are purchasing an item, type in the number next to the item on the product list.")

#                         for (i, item) in enumerate(self.current_cave.for_sale):
#                             print(f"[{i + 1}] {item.name}: ${item.cost}")

#                         print(
#                             f"[{len(self.current_cave.for_sale) + 1}] <Leave shop>")

#                         purchase_num = display.prompt("Please select an item to buy", 1, "int", lambda num: "That isn't a valid item" if num <= 0 or num > (
#                             len(self.current_cave.for_sale) + 1) else True)
#                         # TODO: finish shop
#                     try:
#                         if self.current_cave.name == "Shop":
#                             # Open shop menu
#                             print(
#                                 "This is the shop. A place of safety and where transactions are done.")
#                             print(
#                                 "If you are purchasing an item, type in the name of the item in the product list.")
#                             print(
#                                 "If you are not going to purchase anything, type in leave and exit the menu.")
#                             n = 1
#                             for item in shop_menu:
#                                 # TODO: display the price of the products
#                                 print(f'{n}. {item}: ')
#                                 n += 1
#                             purchase = input("> ")
#                             cost = shop_menu[purchase]
#                             if purchase in shop_menu:
#                                 if self.purse < cost:
#                                     print(
#                                         "You don't have enough money to purchase this item.")
#                                 else:
#                                     self.purse -= cost
#                                     print(
#                                         f'You have successfully purchased {purchase} from the shop.')
#                                     # .pop methods removes the item and its corresponding value from the dictionary permanently
#                                     shop_menu.pop(purchase)
#                                     # add the purchased item into the inventory
#                                     self.items.add(purchase)
#                                     if purchase == "leave":
#                                         self.status_dirty = True

#                             if purchase == "leave":
#                                 self.status_dirty = True
#                     except KeyError:
#                         print("Please enter the name of the item!")
#                         continue

#                 case "items":
#                     for items in self.items:
#                         print(self.items)
#                     if len(self.items) == 0:
#                         print("Empty pockets!")
