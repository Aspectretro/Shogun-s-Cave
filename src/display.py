# Helper functions for handling the terminal UI

import sys
import os
import re


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
    print(f"{message} [y/N] and then press Enter?")
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


def set_raw(stdin):
    """Set the TTY mode to raw for *nix-based systems. No effect on Windows"""
    if os.name == "nt":  # windows
        import msvcrt
    else:  # *nix
        import tty
        import termios
        normal_tty = termios.tcgetattr(stdin)
        tty.setraw(stdin)
        return normal_tty


def set_cooked(stdin, normal_tty):
    """Set the TTY mode back to cooked. Has no effect on Windows"""
    if os.name == "nt":  # windows
        import msvcrt
    else:  # *nix
        import tty
        import termios
        termios.tcsetattr(
            stdin, termios.TCSADRAIN, normal_tty)


def read_raw_char(stdin):
    """Read a single raw character from the tty.

    Must be a raw tty if used on *nix systems
    """

    if os.name == "nt":
        import msvcrt
        char = msvcrt.getwch()
        return str(char)
    else:
        return stdin.read(1)


def alert_box(msg: str):
    """A console-based alert box"""
    clear()
    internal_len = 2 + visual_len(msg)  # 2 spaces padding
    # colour 1 = red
    print(colour(1, f"╔{'═' * internal_len}╗"))  # top row
    print(f"{colour(1, '║')} {msg} {colour(1, '║')}")  # msg row
    print(colour(1, f"╚{'═' * internal_len}╝"))  # bottom row
    print("")  # empty line
    print("> Press Enter to Continue <")
    input()  # wait for enter key
    clear()


def multiline_alert_box(msgs: list[str], colour_code=1):  # colour_code is 1
    """A multi-line console-based alert box. Each line should be its own item in the list"""
    clear()
    # 2 spaces padding, find longest line
    internal_len = 2 + visual_len(max(msgs, key=visual_len))
    print(colour(colour_code, f"╔{'═' * internal_len}╗"))  # top row
    for line in msgs:
        #                                                to account for padding space _______
        print(f"{colour(colour_code, '║')} {line}{' ' * (internal_len - visual_len(line) - 1)}{colour(colour_code, '║')}")
    print(colour(colour_code, f"╚{'═' * internal_len}╝"))  # bottom row
    print("")  # empty line
    print("> Press Enter to Continue <")
    input()  # wait for enter key
    clear()


def speech_box(msg: str, speaker: str, colour_code=1):  # colour_code 1 is red
    """An alert box attributed to a speaker"""
    clear()
    internal_len = 2 + visual_len(msg)  # 2 spaces padding
    speaker_padding = internal_len - 3 - \
        visual_len(speaker)  # space and em dash + speaker
    print(colour(colour_code, f"╔{'═' * internal_len}╗"))  # top row
    print(f"{colour(colour_code, '║')} {msg} {colour(colour_code, '║')}")  # msg row
    print(colour(colour_code, f"║{' ' * internal_len}║"))  # padding row
    # speaker row
    print(f"{colour(colour_code, '║')}{' ' * speaker_padding}— {speaker} {colour(colour_code, '║')}")
    print(colour(colour_code, f"╚{'═' * internal_len}╝"))  # bottom row
    print("")  # empty line
    print("> Press Enter to Continue <")
    input()  # wait for enter key
    clear()


def visual_len(test: str) -> int:
    """Get the visual (column) length of a string by excluding ANSI control characters"""
    # Finding ANSI control characters
    regex = re.compile(
        "[\\u001B\\u009B][[\\]()#;?]*(?:(?:(?:(?:;[-a-zA-Z\\d\\/#&.:=?%@~_]+)*|[a-zA-Z\\d]+(?:;[-a-zA-Z\\d\\/#&.:=?%@~_]*)*)?(?:\\u0007|\\u001B\\u005C|\\u009C))|(?:(?:\\d{1,4}(?:;\\d{0,4})*)?[\\dA-PR-TZcf-nq-uy=><~]))")
    return len(regex.sub("", test))


def print_healthbar(name: str, health: int, max_health: int):
    """Print a coloured healthbar"""
    health_percent = health / max_health

    print(f"{underline(name)}:", colour(
        5, f"{health}/{max_health}HP [{'#' * round(health_percent * 15)}{'_' * round((1 - health_percent) * 15)}]"))
