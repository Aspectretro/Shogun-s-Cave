from game import Game
import display


def main():
    # title screen
    display.clear()
    print("\n")
    print("┏━━━━━━━━━━━━━━━━━━━━━┓")
    print("┣ Shogunate's Caverns ┫")
    print("┗━━━━━━━━━━━━━━━━━━━━━┛")
    print("\033[?25l") # ANSI - try to make cursor invisible
    input("> Press Enter to Start <")
    print("\033[?25h") # make cursor visible again
    game = Game()
    display.clear()
    game.tutorial()
    game.start()

def update():
    pass # TODO: Game and character update goes under here. This is also a main loop.

main()