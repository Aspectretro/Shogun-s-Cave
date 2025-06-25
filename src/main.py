from game import Game


def main():
    # title screen
    # magic numbers: ANSI "clear screen" characters
    print("\033[H\033[J", end="") # clear screen before beginning
    print("\n")
    print("┏━━━━━━━━━━━━━━━━━━━━━┓")
    print("┣ Shogunate's Caverns ┫")
    print("┗━━━━━━━━━━━━━━━━━━━━━┛")
    print("\033[?25l") # ANSI - try to make cursor invisible
    input("> Press Enter to Start <")
    print("\033[?25h") # make cursor visible again
    game = Game()
    print("\033[H\033[J", end="") # clear screen before tutorial
    game.tutorial()
    game.start()

def update():
    pass # TODO: Game and character update goes under here. This is also a main loop.

main()