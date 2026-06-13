"""
Menu base
"""
import datetime
from collections.abc import Callable
from abc import ABC, abstractmethod
from numbers import Number
from typing import Optional


class Menu:
    DIVIDER: str = "════════════════════════════════════════"
    MINOR_DIVIDER: str = "────────────────────────────────────────"

    def __init__(self, options: dict[str, Callable[[], None]], add_quit: bool = False):
        self.options = options
        if add_quit:
            self.options["Quit"] = self.quit

    def header(self) -> str:
        return ""

    def quit(self) -> None:
        """
        Exits the main loop
        """
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

    @staticmethod
    def positive_number(num: float) -> bool:
        return num > 0

    @staticmethod
    def currency_cleaner(string: str) -> str:
        return string.replace('$', '').strip()

    @staticmethod
    def get_currency(text: str) -> float:
        return Menu.get_float(text, Menu.positive_number, Menu.currency_cleaner)

    @staticmethod
    def get_positive_float(text: str) -> float:
        return Menu.get_float(text, Menu.positive_number)

    @staticmethod
    def get_float(text:str, /, test: Optional[Callable[[float], bool]] = None, cleaner: Optional[Callable[[str], str]] = None) -> float:
        """
        Gets a float, that must match the test after the input was cleaned (if a test or cleaner exists)
        :param text: the input text. Exact
        :param test: Optional test, which a cleaned output must meet
        :param cleaner: Optional cleaner, applied to input
        """
        while True:
            try:
                in_str: str = input(text)
                clean: str = in_str if cleaner is None else cleaner(in_str)
                out: float = float(clean)
                if test is not None and not test(out):
                    raise ValueError(f"Test failed for {out}")
                return out
            except ValueError:
                continue

    @staticmethod
    def get_positive_int(text: str):
        return Menu.get_int(text, Menu.positive_number)

    @staticmethod
    def get_int(text:str, /, test: Optional[Callable[[int], bool]] = None, cleaner: Optional[Callable[[str], str]] = None) -> int:
        """
        Gets a float, that must match the test after the input was cleaned (if a test or cleaner exists)
        :raises ValueError if not a valid float or fails the test:
        :param text: the input text. Exact
        :param test: Optional test, which a cleaned output must meet
        :param cleaner: Optional cleaner, applied to input
        """
        while True:
            try:
                in_str: str = input(text)
                clean: str = in_str if cleaner is None else cleaner(in_str)
                out: int = int(clean)
                if test is not None and not test(out):
                    raise ValueError(f"Test failed for {out}")
                return out
            except ValueError:
                continue
        #should never be reached
        return 0

    @staticmethod
    def date_test(text: str) -> bool:
        try:
            date: datetime.date = datetime.date.fromisoformat(text)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_date(text: str) -> datetime.date:
        clean_str: str = Menu.get_str(text, Menu.date_test)
        return datetime.date.fromisoformat(clean_str)

    @staticmethod
    def get_str(text: str, /, test: Optional[Callable[[str], bool]] = None, cleaner: Optional[Callable[[str], str]] = None) -> str:
        """
        Gets a float, that must match the test after the input was cleaned (if a test or cleaner exists)
        :raises ValueError if not a valid float or fails the test:
        :param text: the input text. Exact
        :param test: Optional test, which a cleaned output must meet
        :param cleaner: Optional cleaner, applied to input
        """
        while True:
            try:
                in_str: str = input(text)
                clean: str = in_str if cleaner is None else cleaner(in_str)
                if test is not None and not test(in_str):
                    raise ValueError(f"Test failed for {in_str}")
                return in_str
            except ValueError:
                continue
        #Should never be reached
        return ""