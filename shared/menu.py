"""
Menu base
"""
from abc import ABC, abstractmethod
from typing import Callable


class Menu:
    DIVIDER: str = "════════════════════════════════════════"
    MINOR_DIVIDER: str = "────────────────────────────────────────"

    def __init__(self, options: dict[str, Callable], add_quit: bool = False):
        self.options = options
        if (add_quit):
            self.options["Quit"] = self.quit

    def header(self) -> str:
        return ""

    def quit(self) -> None:
        raise KeyboardInterrupt

    def start(self) -> None:
        if self.header() != "":
            print(self.DIVIDER)
            print(self.header())
            print(self.DIVIDER)

            while True:
                try:
                    self.do_selection()
                except KeyboardInterrupt:
                    break

    def do_selection(self):
        selected: int = self.get_selection()
        option: Callable = list(self.options.values())[selected - 1]
        option()
        print("")
        print(self.DIVIDER)

    def show_menu(self) -> None:
        """
        Shows the menu
        """
        for i in range (0, len(self.options.keys())):
            item = list(self.options.keys())[i]
            print(f"{i+1}. {item}")

    def get_selection(self) -> int:
        while True:
            self.show_menu()
            print(self.DIVIDER)
            print("")
            try:
                selection: int = int(input("> "))

                if selection > len(self.options) or selection < 1:
                    #only allow valid options
                    raise ValueError

                return selection
            except ValueError:
                continue
        #should never be reached
        return -1