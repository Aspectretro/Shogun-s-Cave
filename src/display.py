# Helper functions for handling the terminal UI

import sys

def prompt(message: str, level: int, return_type: str, guard):
    """Prompt the player for a response.

    Level is an integer that represents how "nested" this prompt is e.g. default command prompt is at
    level=0, then a shop is at level=1, etc.

    return_type determines what type the response should be. Valid values are:
        - str
        - int

    Optionally provide a guard lambda expression to validate inputs. The lambda should return True
    on success, otherwise return a str explaining the error. The lambda will receive the converted 
    type (e.g. int) as input.
    """
    # maps return_type to player-understandable names
    type_human_name = {
        "str": "text",
        "int": "whole numbers"
    }
    print(f"{message} · Accepts {bold(type_human_name[return_type])}")
    while True:
        input_msg = bold(f"{level * '>'}> ")
        response = input(input_msg)

        # check guard unless the type needs to be converted
        if guard is not None and return_type != "int":
            checked = guard(response)
            if checked != True:
                print(f"That doesn't seem right: {checked}")
                continue  # loop until a correct response has been obtained

        match return_type:
            case "str":
                # nothing needed to do, return
                return response
            case "int":
                # try to convert to int
                try:
                    int_response = int(response)

                    # check guard with converted type
                    if guard is not None:
                        checked = guard(int_response)
                        if checked != True:
                            print(f"That doesn't seem right: {checked}")
                            continue
                    return int_response
                except ValueError:
                    print(f"That wasn't a valid whole number. Please try again!")
                    continue


def confirm(message: str):
    """Prompt the user with a Y/N confirmation"""
    print(f"{message} [y/N]?")
    try:
        response = sys.stdin.readline().lower()

        if response.startswith('y'):
            return True

        # default to false
        return False
    except:
        return False

def bold(msg: str):
    """Makes the passed text bold in the terminal by adding ANSI codes"""
    return f"\x1B[1m{msg}\x1B[22m"

def dim(msg: str):
    """Makes the passed text dimmer in the terminal by adding ANSI codes"""
    return f"\x1B[2m{msg}\x1B[22m"

def underline(msg: str):
    """Makes the passed text underlined in the terminal by adding ANSI codes"""
    return f"\x1B[4m{msg}\x1B[24m"

def print_hint(hint: str):
    """Print a dimmed hint message, with special characters"""
    print(dim(f"  ╰─ Hint: {hint}"))

def clear():
    """Clears the terminal"""
    print("\033[H\033[J", end="")

def colour(code: int, msg: str):
    """Makes the passed text coloured using ANSI 256-colour codes"""
    return f"\x1B[38;5;{code}m{msg}\x1B[39m"