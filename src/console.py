import display

import os
import sys
import time


class Terminal:
    """A class representing the terminal user interface

    This class handles all tasks related to the displaying text to the user, and
    refreshes to allow for what appears to be dynamic updating
    """

    # Special constants
    ESC = "\033"
    CLEAR = f"{ESC}[H{ESC}[J"

    def __init__(self, prompt="> ", stdin=sys.stdin, stdout=sys.stdout):
        self.prompt = prompt
        self.stdin = stdin
        self.stdout = stdout

        self.is_dirty = True  # whether a refresh is needed
        self.status_lines: list[str] = []
        self.output_lines: list[str] = []
        self.input_line: str = ""  # current input line from player
        self.input_cursor: int = 0  # current input cursor from player

    def start(self):
        """Start the terminal's special handling"""
        # Set the terminal to raw, if not on Windows
        if os.name != "nt":
            import tty
            import termios
            self.normal_tty = termios.tcgetattr(self.stdin)
            tty.setraw(self.stdin)

    def __write(self, text: str):
        """Write and immediately flush to stdout"""
        self.stdout.write(
            f"{self.ESC}[1000D")  # send cursor back to start of line
        self.stdout.write(text)
        self.stdout.flush()

    def __read(self) -> str:
        """Read a single character from input, blocking until one is available"""

        if os.name == "nt":
            import msvcrt
            return str(msvcrt.getwch())

        return self.stdin.read(1)  # on *nix systems read directly from stdin

    def set_status(self, new_lines: list[str]):
        """Update the status message lines"""
        self.is_dirty = True  # set dirty
        self.status_lines = new_lines

    def get_buffer(self) -> list[str]:
        """Get the combined text buffer"""
        buffer = []
        buffer.append(self.status_lines)
        return buffer

    def set_cursor(self, pos: int):
        """Set the output cursor to the specified position"""
        self.__write(f"{self.ESC}[1000D")  # send cursor back to start of line
        self.__write(f"{self.ESC}[{pos}C")

    def output(self, text: str):
        """Add one line of output to the terminal. Will not flush until next refresh

        Equivalent to print()
        """
        self.is_dirty = True
        self.output_lines.append(text)

    def choice_modal(self, title: str, description: str, choices: list, colour_code=7):
        """Displays a modal with choices to the user"""
        self.__write(self.CLEAR)  # clear display

        # 2 spaces padding, find longest line
        internal_len = 2 + \
            display.visual_len(
                max([title, description, *choices], key=display.visual_len))

        # -- write box --
        self.__write(display.colour(
            colour_code, f"╔{'═' * internal_len}╗"))  # top row
        self.__write(display.colour(colour_code, f"║") + ' ' * round((internal_len - 8) / 2) +
                     # title row
                     f" -- {title} -- " + ' ' * round((internal_len - 8) / 2) + display.colour(colour_code, f"║"))

        time.sleep(10)
        self.is_dirty = True

    def refresh(self):
        """Refresh the terminal, rewriting all lines"""
        if not self.is_dirty:
            return  # refresh not needed

        # -- print text --
        # clear display
        self.__write(self.CLEAR)
        self.set_cursor(0)  # reset cursor to start
        for line in self.status_lines:
            self.__write(line + "\n")

        # -- print outputs --
        self.set_cursor(0)
        for line in self.output_lines:
            self.__write(line + "\n")

        # -- print prompt --
        self.__write(self.prompt)
        # set cursor to start of line
        self.set_cursor(0)
        # write input line
        self.__write(self.prompt + self.input_line)
        # set input cursor
        self.set_cursor(len(self.prompt) + self.input_cursor)

        # unset dirty
        self.is_dirty = False

    def read_cmd(self):
        """Special generator function that yields a line every time the user hits Enter"""
        yield ""  # yield empty line to start loop
        self.refresh()
        while True:
            char = self.__read()
            char_code = ord(char)

            # Enter key: yield line
            if char == '\n' or char == '\r':
                line = self.input_line.strip()
                if len(line) == 0:
                    continue  # do not yield empty line
                self.output_lines.append(self.prompt + line)
                yield line
                self.input_line = ""  # clear input
                self.input_cursor = 0  # reset cursor

            # Backspace key
            if char_code == 127 or char_code == 8:
                # delete one character
                if self.input_cursor > 0:
                    self.input_line = self.input_line[:self.input_cursor -
                                                      1] + self.input_line[self.input_cursor:]
                    self.input_cursor -= 1  # move cursor back one

            # -- *nix special character handling --
            #    3 character sequences
            if char_code == 27:  # ESC
                # get char codes of next 2 characters
                next1, next2 = ord(self.__read()), ord(self.__read())

                if next1 == 91:  # keys between letters and numpad
                    if next2 in [50, 53, 54]:
                        # no-op, swallow incoming "~" sign
                        self.__read()

                    if next2 == 51:  # delete key
                        next3 = self.__read()
                        if next3 == "~":
                            # do delete key action
                            self.input_line = self.input_line[:self.input_cursor] + \
                                self.input_line[self.input_cursor + 1:]

                    # arrow keys
                    if next2 == 68:  # left
                        self.input_cursor = max(self.input_cursor - 1, 0)
                    if next2 == 67:  # right
                        self.input_cursor = min(
                            len(self.input_line), self.input_cursor + 1)

            # -- windows special key handling --
            #    2 character sequence
            if char == '\x00':
                next1 = self.__read()

                if next1 == 'K':  # left
                    self.input_cursor = max(self.input_cursor - 1, 0)
                if next1 == 'M':  # right
                    self.input_cursor = min(
                        len(self.input_line), self.input_cursor + 1)

            # -- regular key handling --
            if 32 <= char_code < 127:  # regular ASCII chars
                self.input_line = self.input_line[:self.input_cursor] + \
                    char + self.input_line[self.input_cursor:]
                self.input_cursor += 1

            self.is_dirty = True
            self.refresh()
