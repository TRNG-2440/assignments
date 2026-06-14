"""
Account.py

Defines the abstract base `Account` class and the `AccountType` enum used
throughout the banking system. All concrete account types (Checking,
Savings, Investment) inherit from `Account`.
"""

from abc import ABC, abstractmethod
from enum import IntEnum
import uuid


class AccountType(IntEnum):
    """Enumeration of supported bank account types.

    Inherits from IntEnum so values can be used directly in menus
    (e.g. as numeric choices) while still behaving like named constants.
    """

    CHECKING = 1
    SAVINGS = 2
    INVESTMENT = 3

    def __str__(self) -> str:
        """Returns the lowercased name when called via str(), matching StrEnum behavior."""
        return self.name.lower()


class Account(ABC):
    """Abstract base class representing a generic bank account.

    Stores attributes common to all account types (account number, owner
    name, account type, and balance) and defines the interface that all
    subclasses must implement (`deposit` and `withdraw`).
    """

    def __init__(
        self, customer_name: str, account_type: AccountType, opening_balance: float
    ) -> None:
        """Initialize a new account.

        Args:
            customer_name: The name of the account owner.
            account_type: The type of account (Checking, Savings, Investment).
            opening_balance: The initial balance to deposit into the account.
        """
        # Auto-generate a unique identifier for this account.
        self._account_number: uuid.UUID = uuid.uuid4()
        self._customer_name: str = customer_name
        self._account_type: AccountType = account_type
        self._balance: float = opening_balance

    @property
    def account_number(self) -> uuid.UUID:
        """uuid.UUID: The unique identifier for this account."""
        return self._account_number

    @property
    def customer_name(self) -> str:
        """str: The name of the account owner."""
        return self._customer_name

    @abstractmethod
    def deposit(self, amount: float) -> None:
        """Deposit funds into the account.

        Must be implemented by subclasses.

        Args:
            amount: The amount of money to deposit. Must be positive.
        """
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        """Withdraw funds from the account.

        Must be implemented by subclasses, each enforcing their own rules
        (e.g. overdraft limits, minimum balances, withdrawal limits).

        Args:
            amount: The amount of money to withdraw. Must be positive.
        """
        pass

    def display_account_details(self) -> None:
        """Print a formatted summary of the account's core details.

        Subclasses override this to append additional, type-specific
        information after calling this base implementation.
        """
        print("------------------------------")
        print("Account Details")
        print("------------------------------")
        print(f"Account_id: {self._account_number}")
        print(f"Owner: {self._customer_name}")
        print(f"Account type: {self._account_type}")
        print(f"Balance: ${self._balance}")

    def print_menu(self) -> None:
        """Print the base set of account-level menu options.

        Subclasses extend this with additional options specific to their
        account type and handle the interactive menu loop.
        """
        print("[1] Deposit")
        print("[2] Withdraw")
        print("[3] View Details")
