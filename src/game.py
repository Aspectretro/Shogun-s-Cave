from map import MapGraph
from item import Item
from character import Enemy, Friendly, Boss, Ninja
from cave import Cave, Shop
import display
import parsing

# stdlib
import cmd
import sys
import math


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
        display.clear()
        print("")  # empty line
        print(
            f"Welcome to the {display.bold('Shogunate\'s Caverns!')} This is the tutorial and will show you how the game works.")
        print("")  # empty line
        print(
            f"In this text-based game, you will be dropped into unknown caverns — survive, defeat the {display.colour(1, 'boss')} and find a way out!")
        print(
            f"Throughout your adventure inside this deep, dark world, you will encounter various {display.underline('characters')}, both friend and foe.")
        print(
            f"You can gain valuable {display.colour(220, 'money')} by defeating enemies with weapons bought from the 🛍️  shops!")
        print(
            f"You will start with {display.colour(220, '$20')}. Spend your money wisely, as not all items are of equal usefulness.")
        print("")  # empty line
        print("Press Enter to continue, or type q and then Enter to skip the rest of the tutorial")
        skip = input("> ")
        if skip == "q":
            return  # skip tutorial
        display.clear()
        print(
            f"In these caverns, each cave is given a [{display.bold('number')}] and a name... Use these numbers to refer to the caves you want to move to!")
        print(f"BEWARE! Not all caves are accessible from the start. Explore these caverns... but don't get lost!")
        print("---")
        print("To interact with your environment you can issue commands to the game")
        print("The following commands are available:")
        print("  move:    Move to a connected cave. Specify the number of the cave.")
        print("  fight:   Start a fight with any character in the current cave. You need an item to fight them with!")
        print("  talk:    Talk to a character in the current cave")
        print("  shop:    Open up the shop, if there is one in this cave")
        print("  refresh: Refresh the game window to clear up clutter")
        print("  inv:     Check out your inventory and your money")
        print("  quit:    Quit and close the game")
        print("  help:    Bring up a list of commands")
        print("To issue a command, type the command's name and press Enter")
        display.print_hint(
            "Sometimes, you'll get a hint like this. Pay close attention!")
        print("---")
        print("")
        print("The arrow below indicates the game is listening for some input. Press Enter to continue")
        input("> ")
        display.clear()
        print("Got that? That's the end of the tutorial for now. Good luck on your journey through the Shogunate's Caverns!")
        print("")
        print("> Press Enter to Continue <")
        input()

    def start(self):
        self.cmdloop()

    def set_cave(self, cave_num):
        """Set the current cave by number

        Does nothing if the player is not alive
        """

        if not self.alive:
            return

        if cave_num == self.current_cave.num:
            return  # don't change caves if they are in the same cave already

        # EASTER EGG
        if cave_num == 10 and any(map(lambda item: item.name == "Obsidian Key", self.items)):
            display.multiline_alert_box([
                "A loud rumbling sound fills the cave as an anient hallway breaks apart...",
                "",
                "A shining scroll of text appears as torhes on the walls got lit up one after the other"
            ], colour_code=5)
            display.multiline_alert_box([
                "You've unlocked a pathway to the hall of memorials",
                "A golden door creeked open",
                "There stood three named statues:",
                "",
                "Jim, Max, and Gavin",
            ], colour_code=4)
            display.multiline_alert_box([
                "-*- Credits -*-",
                "Lead Developer: Jim",
                "Assistant Developer: Max",
                "Documentation Expert: Gavin",
                "Diagram Wranglers: Gavin and Max"
            ], colour_code=6)
            return True

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
        self.set_cave(input_int)

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
            name = display.underline(character.name)
            if isinstance(character, Boss):
                name = display.colour(1, name)
            print(f"├╴ [{i + 1}]: {name}")
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
            print(f"├╴ [{i + 1}]: {item.emoji}  {item.name}")
        print(f"╰╴ [{len(self.items) + 1}]: Cancel fight")

        fight_item_int = display.prompt("Please select an item", 1, "int", lambda num: "That isn't an item you have!" if num > len(
            self.items) + 1 or num <= 0 else True)

        if fight_item_int == len(self.items) + 1:
            print("Fight cancelled")
            return

        selected_item = self.items[fight_item_int - 1]

        # Boss battle
        if isinstance(selected_character, Boss):
            # handle boss battle
            won_battle = selected_character.fight(selected_item)
            if not won_battle:
                self.alive = False
                display.multiline_alert_box([
                    f"You use your {display.bold(selected_item.name)}, but the {display.underline(selected_character.name)} doesn't even budge!",
                    "",  # empty line
                    "He strikes you with one fell swoop of his katana...",
                    "",  # 2 empty lines
                    "",
                    display.bold(display.underline(
                        display.colour(1, "GAME OVER!!!")))
                ])
                return True  # stop loop
            else:
                # won!
                display.multiline_alert_box([
                    # Only weapon is crossbow
                    f"You aim your {display.bold('Crossbow')} at the mighty {display.underline(selected_character.name)}...",
                    "",
                    "He lunges at you, shiny katana ready to strike!"],
                    colour_code=1)
                display.multiline_alert_box([
                    f"Suddenly, a mighty thud echoes around the cavern, as the {display.underline(selected_character.name)} falls to the ground",
                    ""
                ], colour_code=2)
                print("")
                print(
                    "CONGRATULATIONS for defeating the final boss and escaping the Shogunate's Caverns!")
                print("")
                print("Press Enter to quit")
                print(
                    "    or press c and Enter to continue exploring the caves (quit anytime with the quit command)")
                choice = input("> ")
                if choice == "c":
                    # Give item
                    self.items.append(selected_character.get_drop())
                    self.__set_dirty()
                    return  # Continue the caves
                else:
                    return True

        # Ninja battles
        if isinstance(selected_character, Ninja):
            selected_character.fight(selected_item)  # execute fight right away
            return

        # Regular battles
        if selected_item.get_damage() == 0:
            print(
                f"You try to use your {display.bold(selected_item.name)} but to no avail! It is not very effective.")
            return

        # Battle sequence
        starting_health = selected_character.get_total_health()
        display.clear()
        display.print_healthbar(selected_character.name,
                                selected_character.get_health(), starting_health)
        print("")  # empty line
        won_fight = selected_character.fight(selected_item)  # execute fight
        print(f"You use your {display.bold(selected_item.name)} to fight the {display.underline(selected_character.name)}, dealing {display.colour(1, min(selected_item.damage, starting_health))} damage!")
        print("> Press Enter to Continue <")
        input()  # wait for enter
        display.clear()
        display.print_healthbar(selected_character.name,
                                selected_character.get_health(), starting_health)
        print("")  # blank line
        if won_fight:
            # give player currency proportional to enemy health
            # function increases at a decreasing rate
            given = round(math.sqrt(20 * starting_health))
            self.purse += given
            print(
                f"Bravo! You have defeated this {display.underline(selected_character.name)}! For this you have received {display.colour(220, f'${given}')}.")
            # remove character from cave
            self.current_cave.remove_character(selected_character)
            # check for dropped items
            items_to_give = selected_character.get_drop()
            print("")  # blank line
            print("> Press Enter to Continue <")
            input()
        else:
            print(
                f"You fight valiantly with your {display.bold(selected_item.name)}, but the {display.underline(selected_character.name)} is not defeated!")
            print("")  # empty line
            print("> Press Enter to Continue <")
            input()

        self.__set_dirty()

        # FEAT: Fight sequence

    def do_talk(self, arg):
        """Start a conversation with a specific character"""
        characters = self.current_cave.characters
        if not len(characters):
            print("There is no one here to talk to!")
            return

        print("Select a character to talk to by inputting the numbers next to their name")

        for (i, character) in enumerate(characters):
            # print i + 1 next to characters' names
            name = display.underline(character.name)
            if isinstance(character, Boss):
                name = display.colour(1, name)
            print(f"├╴ [{i + 1}]: {name}")
            print(f"│    └╌╌ {character.description}")
        print(f"╰╴ [{len(characters) + 1}]: Cancel conversation")

        talk_with_int = display.prompt("Please select a character", 1, "int",
                                       lambda num: "That isn't a valid option" if num > len(characters) + 1 or num <= 0 else True)

        if talk_with_int == (len(characters) + 1):
            # cancel talk
            print("")
            return

        selected_character = characters[talk_with_int - 1]

        if selected_character.conversation is None:
            print(
                f"This {selected_character.name} doesn't want to talk to you.")
            return

        display.speech_box(selected_character.conversation,
                           selected_character.name, colour_code=8)
        self.__set_dirty()

    def do_shop(self, arg):
        """Open up the shop in this cave, if there is one"""
        # FEAT: Shopping system
        if not isinstance(self.current_cave, Shop):
            print("There isn't a shop here!")
            display.print_hint(
                "You can only open the shop in caves that have a shop in them!")
            return

        if not len(self.current_cave.for_sale):  # out of stock! (no items for sale)
            print("This shop is out of stock!")
            return

        print(
            f"Welcome to the shop in cave {display.bold(self.current_cave.num)}, a place of safety where transactions are done.")
        print("Please select the item you wish to purchase by entering its number in brackets!")

        print(f"You have {display.colour(220, f'${self.purse}')
                          } | The following items are for sale:")

        for (i, item) in enumerate(self.current_cave.for_sale):
            cost_display = f"${item.cost}"
            # if the player cannot afford the item, colour it red
            if item.cost > self.purse:
                cost_display = display.colour(160, cost_display)
            else:  # else make it green
                cost_display = display.colour(34, cost_display)
            print(f"├╴ [{i + 1}] {item.emoji} {item.name} ({cost_display})")
            print(f"│    └╌╌ {item.description}")
        print(
            f"╰╴ [{len(self.current_cave.for_sale) + 1}] Leave without buying anything")

        item_int = display.prompt("Please select an item", 1, "int", lambda num: "That isn't a valid item!" if num > (len(
            self.current_cave.for_sale) + 1) or num <= 0 else True)

        if item_int == len(self.current_cave.for_sale) + 1:
            # exit shop
            print("Leaving the shop!")
            return

        # handle buying items
        item_selected = self.current_cave.for_sale[item_int - 1]

        if item_selected.cost > self.purse:
            print(
                f"Hey! You can't afford that item. You only have {display.colour(220, f'${self.purse}')}")
            return

        # add to player's items, remove from shop items
        self.items.append(item_selected)
        self.current_cave.remove_shop_item(item_selected)
        self.purse -= item_selected.cost

        print(f"You've bought a brand new {display.bold(f'{item_selected.emoji} {item_selected.name}')}! You now have {
              display.colour(220, f'${self.purse}')}.")

    def do_inv(self, arg):
        """Check what items you currently have and show how much money you've got"""
        if not len(self.items):
            print(
                f"You don't have any items right now, and {display.colour(220, f'${self.purse}')}")
            display.print_hint("Items can be found or bought in a 🛍️  shop")
            return

        print(
            f"You have {display.bold(len(self.items))} item(s) and {display.colour(220, f'${self.purse}')}")
        for (i, item) in enumerate(self.items):
            if i == len(self.items) - 1:  # last item has a different special character
                print(f"╰╴ {item.emoji} {item.name}")
            else:
                print(f"├╴ {item.emoji} {item.name}")

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
                            if isinstance(character, Boss):
                                # bosses are red
                                print(
                                    f"  The {display.colour(1, display.underline(character.name))}: {character.description}")
                            else:
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
                    self.stdout.write(display.dim("(command)"))
                    # send cursor to correct starting location
                    self.stdout.write("\033[1000D")
                    self.stdout.write(f"\033[{len(self.prompt)}C")
                    self.stdout.flush()
                    # Construct a line from reading each character from stdin
                    line = ""
                    cursor = 0  # position of typing cursor
                    # set tty to raw to disable buffering
                    normal_tty = display.set_raw(self.stdin)
                    while True:
                        char = display.read_raw_char(
                            self.stdin)  # read one character
                        char_code = ord(char)

                        # user hit enter key
                        if char == '\r' or char == '\n':
                            break  # exit

                        # backspace key
                        if char_code == 127 or char_code == 8:  # ASCII 8: windows backspace
                            # delete one character
                            if cursor > 0:
                                line = line[:cursor - 1] + line[cursor:]
                            cursor = max(cursor - 1, 0)

                        # special key handling (*nix '[' sequence),
                        # 3 character sequences starting with [
                        if char_code == 27:  # '['
                            next1, next2 = ord(display.read_raw_char(self.stdin)), ord(
                                display.read_raw_char(self.stdin))

                            if next1 == 91:  # keys between letters and numpad
                                if next2 in [50, 53, 54]:  # ins, pgup, pgdn
                                    next3 = display.read_raw_char(self.stdin)
                                    # no op, just swallow "~" sign

                                if next2 == 51:  # delete key
                                    next3 = display.read_raw_char(self.stdin)
                                    if next3 == "~":
                                        line = line[:cursor] + \
                                            line[cursor + 1:]

                                # arrow keys
                                if next2 == 68:  # left
                                    cursor = max(cursor - 1, 0)
                                if next2 == 67:  # right
                                    cursor = min(
                                        len(line), cursor + 1)

                        # special key handling (win)
                        # 2 character sequence starting with \x00
                        if char == '\x00':  # char_code == 48
                            next_char = display.read_raw_char(
                                self.stdin)  # get next char

                            if next_char == 'K':  # left arrow
                                cursor = max(cursor - 1, 0)

                            if next_char == 'M':  # right arrow
                                cursor = min(len(line), cursor + 1)

                        # if character is regular ASCII character
                        # add to line buffer and +1 to index
                        if 32 <= char_code < 127:
                            line = line[:cursor] + char + line[cursor:]
                            cursor += 1

                        # refresh (erase and reprint) buffered line
                        # send cursor to line start
                        self.stdout.write("\033[1000D")
                        self.stdout.write("\033[0K")  # erase line
                        self.stdout.write(self.prompt + line)  # re-print line
                        if len(line) == 0:
                            self.stdout.write(display.dim("(command)"))
                        # send cursor to line start
                        self.stdout.write("\033[1000D")
                        # set cursor pos
                        self.stdout.write(f"\033[{cursor + len(self.prompt)}C")
                        self.stdout.flush()  # flush to terminal
                    # loop done, reset tty to normal
                    display.set_cooked(self.stdin, normal_tty)
                    print("")  # Print newline

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
