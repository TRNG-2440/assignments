"""
Bank.py

Defines the `Bank` class, which manages a collection of accounts, and
provides the CLI menu loop that drives the PyBank application.
"""

from typing import Optional
from uuid import UUID

from Account import Account, AccountType
from AccountFactory import AccountFactory
from custom_exceptions import (
    InvalidInputError,
    UnknownAccountError,
)
from utils import try_cast_to_float, try_cast_to_int


class Bank:
    """Manages a collection of bank accounts and the top-level CLI menu."""

    def __init__(self) -> None:
        """Initialize the bank with an empty set of accounts."""
        self.name: str = "PyBank"
        self.__accounts: dict[UUID, Account] = {}

    def print_menu(self):
        """Print the top-level main menu options."""
        print("==============================")
        print(f"Welcome to {self.name} CLI")
        print("==============================")
        print("[1] Open a new account")
        print("[2] Select an account")
        print("[3] List all accounts")
        print("[4] Quit")

    def create_account(self, account_type: AccountType, **kwargs) -> None:
        """Create a new account, register it with the bank, and display its details.

        Args:
            account_type: The type of account to open.
            **kwargs: Additional arguments required by the specific account
                type (e.g. `customer_name`, `opening_balance`, `roi`).
        """
        # Delegate construction of the correct account subclass to the factory.
        account: Account = AccountFactory.create_account(account_type, **kwargs)
        # Register the newly created account so it can be looked up later.
        self.__accounts[account.account_number] = account
        account.display_account_details()

    def __get_account(self, account_number: UUID) -> Optional[Account]:
        """Look up an account by its account number.

        Args:
            account_number: The UUID of the account to find.

        Returns:
            The matching `Account`, or `None` if no account with that
            number exists.
        """
        return self.__accounts.get(account_number)

    def select_account(self, account_number: UUID) -> None:
        """Select an account and enter its account-specific menu loop.

        Args:
            account_number: The UUID of the account to select.

        Raises:
            UnknownAccountError: If no account with the given number exists.
        """
        account = self.__get_account(account_number)

        if not account:
            raise UnknownAccountError(account_number)

        print(f"Account selected: {account.customer_name} ({account.account_number})")
        try:
            # Hand control over to the account's own interactive menu loop.
            account.print_menu()
        except Exception as e:
            print(e)

    def list_all_accounts(self):
        """Print the details of every account currently managed by the bank."""
        for account in self.__accounts.values():
            account.display_account_details()
            print()

    @staticmethod
    def print_account_types() -> None:
        """Print the list of supported account types and their numeric codes."""
        for account_type in AccountType:
            print(f"[{account_type.value}] {str(account_type)}")


if __name__ == "__main__":
    bank = Bank()
    bank.print_menu()

    while True:
        action = 0
        try:
            action = try_cast_to_int(prompt="> ")
        except InvalidInputError as e:
            print(e)

        match action:
            case 1:
                # --- Open a new account ---
                bank.print_account_types()
                try:
                    account_type: AccountType = AccountType(
                        try_cast_to_int(prompt="Account type: ")
                    )
                    customer_name: str = input("Owner name: ")
                    opening_balance: float = try_cast_to_float(
                        prompt="Opening Balance: "
                    )  # type: ignore
                    if account_type == AccountType.INVESTMENT:
                        # Investment accounts also require an initial rate of return.
                        roi: float = try_cast_to_float(
                            prompt="Enter rate of investment: "
                        )  # type: ignore
                        bank.create_account(
                            account_type=account_type,
                            customer_name=customer_name,
                            opening_balance=opening_balance,
                            roi=roi,
                        )
                    else:
                        bank.create_account(
                            account_type=account_type,
                            customer_name=customer_name,
                            opening_balance=opening_balance,
                        )
                except Exception as e:
                    print(e)

            case 2:
                # --- Select an existing account ---
                try:
                    account_number = UUID(input("Enter account number: "))
                    bank.select_account(account_number)
                except Exception as e:
                    print(e)

            case 3:
                # --- List all accounts ---
                bank.list_all_accounts()
            case 4:
                # --- Quit the application ---
                break
            case _:
                print("Invalid choice! Try again..")
