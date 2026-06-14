"""
InvestmentAccount.py

Defines the `InvestmentAccount` class, a concrete `Account` subclass that
enforces a minimum balance requirement and supports applying a variable
rate of return to simulate investment growth.
"""

from Account import Account, AccountType
from custom_exceptions import (
    InsufficientFundsException,
    InvalidAmountError,
    InvalidInputError,
)
from utils import try_cast_to_float, try_cast_to_int

# The minimum balance the account must maintain at all times.
MINIMUM_BALANCE = 200


class InvestmentAccount(Account):
    """An investment account with a minimum balance and a configurable return rate.

    Withdrawals that would drop the balance below `MINIMUM_BALANCE` are
    rejected. The account also supports applying a return rate (ROI) to
    simulate investment growth, and changing that rate over time.
    """

    def __init__(
        self,
        customer_name: str,
        account_type: AccountType,
        opening_balance: float,
        roi: float,
    ) -> None:
        """Initialize an investment account.

        Args:
            customer_name: The name of the account owner.
            account_type: The account type (expected to be INVESTMENT).
            opening_balance: The initial balance for the account. Must be
                at least `MINIMUM_BALANCE`.
            roi: The initial rate of return (as a percentage) applied via
                `apply_return_rate`.

        Raises:
            InsufficientFundsException: If `opening_balance` is below
                `MINIMUM_BALANCE`.
        """
        # The opening balance must already satisfy the minimum balance
        # requirement before the account can be created.
        if opening_balance < MINIMUM_BALANCE:
            raise InsufficientFundsException(MINIMUM_BALANCE - opening_balance)
        super().__init__(customer_name, account_type, opening_balance)
        self._return_rate: float = roi

    def deposit(self, amount: float) -> None:
        """Deposit funds into the investment account.

        Args:
            amount: The amount to deposit. Must be positive.

        Raises:
            InvalidAmountError: If `amount` is zero or negative.
        """
        if amount <= 0:
            raise InvalidAmountError(amount)
        self._balance += amount
        print(f"Deposited ${amount}. New balance: ${self._balance}")

    def withdraw(self, amount: float) -> None:
        """Withdraw funds, enforcing the minimum balance requirement.

        Args:
            amount: The amount to withdraw. Must be positive.

        Raises:
            InvalidAmountError: If `amount` is zero or negative.
            InsufficientFundsException: If the withdrawal would drop the
                balance below `MINIMUM_BALANCE`.
        """
        if amount <= 0:
            raise InvalidAmountError(amount)

        # Reject the withdrawal if it would bring the balance below the
        # required minimum.
        if self._balance - amount < MINIMUM_BALANCE:
            raise InsufficientFundsException(amount - (self._balance - MINIMUM_BALANCE))

        self._balance -= amount
        print(f"Withdrew ${amount}. New balance: ${self._balance}")

    def apply_return_rate(self) -> None:
        """Apply the current return rate to the balance, simulating investment growth."""
        self._balance += (self._return_rate / 100) * self._balance
        print(
            f"Applied return rate ({self._return_rate}%). New balance: {self._balance}"
        )

    def change_return_rate(self, return_rate_percent: float) -> None:
        """Update the account's return rate and immediately apply it.

        Args:
            return_rate_percent: The new rate of return, as a percentage.
        """
        print(f"ROI changed from {self._return_rate} to {return_rate_percent}")
        self._return_rate = return_rate_percent
        self.apply_return_rate()

    def display_account_details(self) -> None:
        """Print account details, including the current return on investment rate."""
        super().display_account_details()
        print(f"Return on investment: {self._return_rate}%")
        print("------------------------------")

    def print_menu(self) -> None:
        """Display the investment account menu and run its interactive loop.

        Supports depositing, withdrawing, viewing details, applying the
        current ROI, changing the ROI, and returning to the main menu.
        """
        super().print_menu()
        print("[4] Apply ROI")
        print("[5] Change ROI")
        print("[6] Back to main menu")

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
                    # Apply the current return rate to the balance.
                    self.apply_return_rate()
                case 5:
                    # Change the return rate and apply it immediately.
                    try:
                        roi = try_cast_to_float(prompt="Rate of investment: ")
                        if roi:
                            self.change_return_rate(roi)
                    except Exception as e:
                        print(e)
                case 6:
                    # Return to the main menu.
                    break
                case _:
                    print("Invalid choice! Try again..")
