"""
custom_exceptions.py

Defines the custom exception classes used throughout the banking system to
signal invalid operations (e.g. negative deposits, exceeded overdraft or
withdrawal limits, insufficient funds, unknown account types/numbers, and
invalid CLI input) with clear, descriptive error messages.
"""

from uuid import UUID

from Account import AccountType


class InvalidAmountError(ValueError):
    """Raised when a deposit or withdrawal amount is zero or negative."""

    def __init__(self, amount: float) -> None:
        """Initialize the error.

        Args:
            amount: The invalid amount that was provided.
        """
        self.deposit_amount = amount
        super().__init__(
            f"Invalid amount: ${self.deposit_amount}. Amount must be positive"
        )


class OverdraftLimitExceededError(ValueError):
    """Raised when a withdrawal would exceed a checking account's overdraft limit."""

    def __init__(self, balance: float, overdraft_amount_left: float) -> None:
        """Initialize the error.

        Args:
            balance: The account's current balance.
            overdraft_amount_left: The amount of overdraft buffer still
                available before the limit is reached.
        """
        self.balance = balance
        self.overdraft_amount_left = overdraft_amount_left
        super().__init__(
            f"Overdraft limit exceeded! Current balance: {self.balance} Overdraft amount remaining: {self.overdraft_amount_left}"
        )


class WithdrawLimitExceededError(ValueError):
    """Raised when a savings account has reached its monthly withdrawal limit."""

    def __init__(self, max_withdraws: int, used_withdraws: int) -> None:
        """Initialize the error.

        Args:
            max_withdraws: The maximum number of withdrawals allowed per month.
            used_withdraws: The number of withdrawals already used this month.
        """
        self.max_withdraws = max_withdraws
        self.used_withdraws = used_withdraws
        super().__init__(
            f"Monthly withdrawal limit reached ({self.used_withdraws}/{self.max_withdraws} used)! Try again next month.."
        )


class InsufficientFundsException(ValueError):
    """Raised when a withdrawal would drop a balance below an allowed minimum.

    Used for both savings accounts (minimum balance of zero) and investment
    accounts (a fixed minimum balance requirement).
    """

    def __init__(self, shortfall: float) -> None:
        """Initialize the error.

        Args:
            shortfall: The amount by which the requested withdrawal exceeds
                the available/allowed funds.
        """
        self.shortfall = shortfall
        super().__init__(f"Insufficient funds! Balance short by ${self.shortfall}")


class UnknownAccountTypeError(ValueError):
    """Raised when the `AccountFactory` is asked to create an unsupported account type."""

    def __init__(self, account_type: AccountType) -> None:
        """Initialize the error.

        Args:
            account_type: The unrecognized account type that was requested.
        """
        self.account_type = account_type
        super().__init__(f"Unknown account type: {str(account_type)} encountered!")


class UnknownAccountError(ValueError):
    """Raised when looking up an account number that does not exist in the bank."""

    def __init__(self, account_number: UUID) -> None:
        """Initialize the error.

        Args:
            account_number: The account number that could not be found.
        """
        self.account_number = account_number
        super().__init__(f"Account number {self.account_number} does not exist!")


class InvalidInputError(ValueError):
    """Raised when user-provided CLI input cannot be converted to the expected type."""

    def __init__(self, *args: object) -> None:
        """Initialize the error.

        Args:
            *args: Arguments forwarded to `ValueError.__init__`, typically a
                descriptive error message.
        """
        super().__init__(*args)
