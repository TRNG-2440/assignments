"""
CheckingAccount.py

Defines the `CheckingAccount` class, a concrete `Account` subclass that
supports overdraft protection up to a fixed limit, with an overdraft fee
applied whenever the account is overdrawn.
"""

from Account import Account, AccountType
from custom_exceptions import (
    InvalidAmountError,
    InvalidInputError,
    OverdraftLimitExceededError,
)
from utils import try_cast_to_float, try_cast_to_int

# Maximum amount the account may be overdrawn beyond a zero balance.
OVERDRAFT_LIMIT = 100
# Flat fee charged whenever a withdrawal causes the account to go into (or
# deeper into) overdraft.
OVERDRAFT_FEE = 10


class CheckingAccount(Account):
    """A checking account with overdraft protection.

    Withdrawals that would exceed the current balance are allowed to draw
    against an overdraft buffer of up to `OVERDRAFT_LIMIT`. Any withdrawal
    that pushes the account into (or further into) overdraft incurs a flat
    `OVERDRAFT_FEE`.
    """

    def __init__(
        self, customer_name: str, account_type: AccountType, opening_balance: float
    ) -> None:
        """Initialize a checking account.

        Args:
            customer_name: The name of the account owner.
            account_type: The account type (expected to be CHECKING).
            opening_balance: The initial balance for the account.
        """
        super().__init__(customer_name, account_type, opening_balance)
        # Tracks how much of the overdraft buffer is currently in use.
        self._overdraft_amount_used: float = 0

    def deposit(self, amount: float) -> None:
        """Deposit funds, paying down any outstanding overdraft first.

        If the account is currently overdrawn, the deposit first reduces
        the outstanding overdraft amount before increasing the balance.

        Args:
            amount: The amount to deposit. Must be positive.

        Raises:
            InvalidAmountError: If `amount` is zero or negative.
        """
        if amount <= 0:
            raise InvalidAmountError(amount)

        # If the account is in overdraft, use all of this
        # deposit to pay down the outstanding overdraft amount first.
        if self._balance < 0 and self._overdraft_amount_used > 0:
            self._overdraft_amount_used -= (
                amount
                if self._overdraft_amount_used >= amount
                else self._overdraft_amount_used
            )
        self._balance += amount
        print(
            f"Deposited ${amount}. New balance: ${self._balance} Overdraft amount used: ${self._overdraft_amount_used}"
        )

    def withdraw(self, amount: float) -> None:
        """Withdraw funds, drawing on the overdraft buffer if necessary.

        Args:
            amount: The amount to withdraw. Must be positive.

        Raises:
            InvalidAmountError: If `amount` is zero or negative.
            OverdraftLimitExceededError: If the withdrawal would cause the
                overdraft usage to exceed `OVERDRAFT_LIMIT`.
        """
        if amount <= 0:
            raise InvalidAmountError(amount)

        # Reject the withdrawal if it would push overdraft usage past the
        # allowed limit.
        if (
            self._balance <= 0
            and self._overdraft_amount_used + amount > OVERDRAFT_LIMIT
        ):
            raise OverdraftLimitExceededError(
                self._balance, OVERDRAFT_LIMIT - self._overdraft_amount_used
            )

        # This withdrawal causes (or continues) an overdraft: track how
        # much of the overdraft buffer is used and apply the overdraft fee.
        if self._balance <= 0 or self._balance - amount < 0:
            self._overdraft_amount_used += (
                amount if self._balance <= 0 else amount - self._balance
            )
            self._balance -= amount + OVERDRAFT_FEE
        else:
            # Sufficient funds available; withdraw normally with no fee.
            self._balance -= amount

        print(
            f"Withdrew ${amount}. New balance: ${self._balance} Overdraft amount used: ${self._overdraft_amount_used}"
        )

    def display_account_details(self) -> None:
        """Print account details, including overdraft-related information."""
        super().display_account_details()
        print(f"Overdraft limit: ${OVERDRAFT_LIMIT}")
        print(f"Overdraft amount used: ${self._overdraft_amount_used}")
        print(f"Overdraft fee: ${OVERDRAFT_FEE}")
        print("------------------------------")

    def print_menu(self) -> None:
        """Display the checking account menu and run its interactive loop.

        Supports depositing, withdrawing, viewing details, and returning
        to the main menu.
        """
        super().print_menu()
        print("[4] Back to main menu")

        while True:
            action = 0
            try:
                action = try_cast_to_int(prompt="> ")
            except InvalidInputError as e:
                print(e)

            match action:
                case 1:
                    # Deposit funds into the account.
                    try:
                        amount = try_cast_to_float(prompt="Deposit amount: ")
                        if amount:
                            self.deposit(amount)
                    except Exception as e:
                        print(e)
                case 2:
                    # Withdraw funds from the account.
                    try:
                        amount = try_cast_to_float(prompt="Withdraw amount: ")
                        if amount:
                            self.withdraw(amount)
                    except Exception as e:
                        print(e)

                case 3:
                    # Show this account's details.
                    self.display_account_details()
                case 4:
                    # Return to the main menu.
                    break
                case _:
                    print("Invalid choice! Try again..")
