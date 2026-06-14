"""
SavingsAccount.py

Defines the `SavingsAccount` class, a concrete `Account` subclass that
enforces a monthly withdrawal limit and supports applying a monthly
interest rate to the balance.
"""

from Account import Account, AccountType
from custom_exceptions import (
    InsufficientFundsException,
    InvalidAmountError,
    WithdrawLimitExceededError,
)
from utils import try_cast_to_float, try_cast_to_int

# Interest rate (percent) applied to the balance when `apply_monthly_interest` is called.
MONTHLY_INTEREST_RATE = 2.5
# Maximum number of withdrawals permitted per month before the limit is reached.
MAX_WITHDRAWALS_PER_MONTH = 3


class SavingsAccount(Account):
    """A savings account with a monthly withdrawal limit and interest accrual.

    Tracks the number of withdrawals made during the current month and
    rejects any withdrawal beyond `MAX_WITHDRAWALS_PER_MONTH`. Applying
    monthly interest increases the balance by `MONTHLY_INTEREST_RATE`
    percent and resets the withdrawal counter.
    """

    def __init__(
        self, customer_name: str, account_type: AccountType, opening_balance: float
    ) -> None:
        """Initialize a savings account.

        Args:
            customer_name: The name of the account owner.
            account_type: The account type (expected to be SAVINGS).
            opening_balance: The initial balance for the account.
        """
        super().__init__(customer_name, account_type, opening_balance)
        # Number of withdrawals made so far during the current month.
        self._withdrawals_used: int = 0

    def deposit(self, amount: float) -> None:
        """Deposit funds into the savings account.

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
        """Withdraw funds, enforcing the monthly withdrawal limit.

        Args:
            amount: The amount to withdraw. Must be positive.

        Raises:
            InvalidAmountError: If `amount` is zero or negative.
            WithdrawLimitExceededError: If the monthly withdrawal limit has
                already been reached.
            InsufficientFundsException: If the withdrawal would result in a
                negative balance.
        """
        if amount <= 0:
            raise InvalidAmountError(amount)

        # Reject the withdrawal if the monthly limit has already been used up.
        if self._withdrawals_used >= MAX_WITHDRAWALS_PER_MONTH:
            raise WithdrawLimitExceededError(
                MAX_WITHDRAWALS_PER_MONTH, self._withdrawals_used
            )

        # Savings accounts cannot go negative.
        if self._balance - amount < 0:
            raise InsufficientFundsException(amount - self._balance)

        self._balance -= amount
        self._withdrawals_used += 1
        print(f"Withdrew ${amount}. New balance: ${self._balance}")

    def apply_monthly_interest(self) -> None:
        """Apply the monthly interest rate to the balance and reset withdrawal count.

        Increases the balance by `MONTHLY_INTEREST_RATE` percent and resets
        `_withdrawals_used` back to zero, simulating the start of a new month.
        """
        self._balance += (MONTHLY_INTEREST_RATE / 100) * self._balance
        print(
            f"Applied monthly interest ({MONTHLY_INTEREST_RATE}%). New balance: {self._balance}"
        )
        # A new month resets the withdrawal counter.
        self._withdrawals_used = 0

    def display_account_details(self) -> None:
        """Print account details, including withdrawal usage and interest rate."""
        super().display_account_details()
        print(
            f"Monthly withdrawals used: {self._withdrawals_used}/{MAX_WITHDRAWALS_PER_MONTH}"
        )
        print(f"Monthly interest rate: {MONTHLY_INTEREST_RATE}%")
        print("------------------------------")

    def print_menu(self) -> None:
        """Display the savings account menu and run its interactive loop.

        Supports depositing, withdrawing, viewing details, applying monthly
        interest, and returning to the main menu.
        """
        super().print_menu()
        print("[4] Apply monthly interest")
        print("[5] Back to main menu")

        while True:
            action = 0
            try:
                action = try_cast_to_int(prompt="> ")
            except Exception as e:
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
                    # Apply monthly interest and reset the withdrawal counter.
                    self.apply_monthly_interest()
                case 5:
                    # Return to the main menu.
                    break
                case _:
                    print("Invalid choice! Try again..")
