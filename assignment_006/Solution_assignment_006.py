import random
import string

class BankingError(Exception):
    """Base exception for all banking errors."""


class InvalidAmountError(BankingError):
    """Raised when a deposit or withdrawal amount is invalid."""


class OverdraftExceededError(BankingError):
    """Raised when a withdrawal would exceed the overdraft limit."""


class WithdrawalLimitError(BankingError):
    """Raised when the monthly withdrawal limit has been reached."""


class MinimumBalanceError(BankingError):
    """Raised when a withdrawal would drop the balance below the minimum."""


class AccountNotFoundError(BankingError):
    """Raised when an account number cannot be found."""

class Account:
    """Base class representing a generic bank account."""

    _PREFIX = "ACC"

    def __init__(self, owner: str, opening_balance: float):
        if opening_balance < 0:
            raise InvalidAmountError("Opening balance cannot be negative.")
        self._owner = owner
        self._account_number = self._generate_account_number()
        self._balance = opening_balance

    # --- internal helpers ---------------------------------------------------

    def _generate_account_number(self) -> str:
        digits = "".join(random.choices(string.digits, k=5))
        return f"{self._PREFIX}-{digits}"

    def _validate_positive_amount(self, amount: float, label: str = "Amount") -> None:
        if not isinstance(amount, (int, float)):
            raise InvalidAmountError(f"{label} must be a number.")
        if amount <= 0:
            raise InvalidAmountError(f"{label} must be greater than zero (got {amount}).")

    # --- public interface ---------------------------------------------------

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        self._validate_positive_amount(amount, "Deposit amount")
        self._balance += amount
        print(f"Deposited ${amount:,.2f}. New balance: ${self._balance:,.2f}")

    def withdraw(self, amount: float) -> None:
        """Base withdrawal — subclasses override with their own rules."""
        self._validate_positive_amount(amount, "Withdrawal amount")
        if amount > self._balance:
            raise OverdraftExceededError(
                f"Insufficient funds. Balance: ${self._balance:,.2f}, "
                f"Requested: ${amount:,.2f}."
            )
        self._balance -= amount
        print(f"Withdrew ${amount:,.2f}. New balance: ${self._balance:,.2f}")

    def display_details(self) -> None:
        print("-" * 30)
        print("Account Details")
        print("-" * 30)
        print(f"{'Owner':<12}: {self._owner}")
        print(f"{'Account #':<12}: {self._account_number}")
        print(f"{'Type':<12}: {self.__class__.__name__.replace('Account', ' Account').strip()}")
        print(f"{'Balance':<12}: ${self._balance:,.2f}")
        print("-" * 30)

    def __str__(self) -> str:
        return f"{self._owner} ({self._account_number}) — ${self._balance:,.2f}"

class CheckingAccount(Account):
    """
    Checking account with overdraft protection.
    Withdrawals may dip into the overdraft buffer but not beyond it.
    """

    _PREFIX = "CHK"
    DEFAULT_OVERDRAFT_LIMIT = 500.0

    def __init__(self, owner: str, opening_balance: float,
                 overdraft_limit: float = DEFAULT_OVERDRAFT_LIMIT):
        super().__init__(owner, opening_balance)
        if overdraft_limit < 0:
            raise InvalidAmountError("Overdraft limit cannot be negative.")
        self._overdraft_limit = overdraft_limit

    @property
    def overdraft_limit(self) -> float:
        return self._overdraft_limit

    def withdraw(self, amount: float) -> None:
        self._validate_positive_amount(amount, "Withdrawal amount")
        available = self._balance + self._overdraft_limit
        if amount > available:
            raise OverdraftExceededError(
                f"Overdraft limit exceeded. Available (including overdraft): "
                f"${available:,.2f}, Requested: ${amount:,.2f}."
            )
        self._balance -= amount
        if self._balance < 0:
            print(
                f"Withdrew ${amount:,.2f}. New balance: ${self._balance:,.2f} "
                f"(overdraft used: ${abs(self._balance):,.2f})"
            )
        else:
            print(f"Withdrew ${amount:,.2f}. New balance: ${self._balance:,.2f}")

    def display_details(self) -> None:
        print("-" * 30)
        print("Account Details")
        print("-" * 30)
        print(f"{'Owner':<12}: {self._owner}")
        print(f"{'Account #':<12}: {self._account_number}")
        print(f"{'Type':<12}: Checking")
        print(f"{'Balance':<12}: ${self._balance:,.2f}")
        overdraft_used = max(0.0, -self._balance)
        print(f"{'Overdraft':<12}: ${overdraft_used:,.2f} used / ${self._overdraft_limit:,.2f} limit")
        print("-" * 30)

class SavingsAccount(Account):
    """
    Savings account with monthly interest and a withdrawal limit.
    """

    _PREFIX = "SAV"
    DEFAULT_INTEREST_RATE = 0.025   # 2.5 %
    DEFAULT_WITHDRAWAL_LIMIT = 3

    def __init__(self, owner: str, opening_balance: float,
                 interest_rate: float = DEFAULT_INTEREST_RATE,
                 withdrawal_limit: int = DEFAULT_WITHDRAWAL_LIMIT):
        super().__init__(owner, opening_balance)
        if interest_rate < 0:
            raise InvalidAmountError("Interest rate cannot be negative.")
        if withdrawal_limit < 1:
            raise InvalidAmountError("Withdrawal limit must be at least 1.")
        self._interest_rate = interest_rate
        self._withdrawal_limit = withdrawal_limit
        self._withdrawals_this_month = 0

    @property
    def interest_rate(self) -> float:
        return self._interest_rate

    @property
    def withdrawals_this_month(self) -> int:
        return self._withdrawals_this_month

    @property
    def withdrawal_limit(self) -> int:
        return self._withdrawal_limit

    def withdraw(self, amount: float) -> None:
        self._validate_positive_amount(amount, "Withdrawal amount")
        if self._withdrawals_this_month >= self._withdrawal_limit:
            raise WithdrawalLimitError(
                f"Monthly withdrawal limit reached "
                f"({self._withdrawals_this_month}/{self._withdrawal_limit} used). "
                f"Try again next month."
            )
        if amount > self._balance:
            raise OverdraftExceededError(
                f"Insufficient funds. Balance: ${self._balance:,.2f}, "
                f"Requested: ${amount:,.2f}."
            )
        self._balance -= amount
        self._withdrawals_this_month += 1
        print(
            f"Withdrew ${amount:,.2f}. New balance: ${self._balance:,.2f} "
            f"({self._withdrawals_this_month}/{self._withdrawal_limit} withdrawals used)"
        )

    def apply_monthly_interest(self) -> None:
        """Apply the monthly interest rate to the current balance."""
        interest = self._balance * self._interest_rate
        self._balance += interest
        self._withdrawals_this_month = 0  # reset counter at month boundary
        print(
            f"Applied monthly interest ({self._interest_rate * 100:.1f}%). "
            f"New balance: ${self._balance:,.2f}"
        )

    def display_details(self) -> None:
        print("-" * 30)
        print("Account Details")
        print("-" * 30)
        print(f"{'Owner':<12}: {self._owner}")
        print(f"{'Account #':<12}: {self._account_number}")
        print(f"{'Type':<12}: Savings")
        print(f"{'Balance':<12}: ${self._balance:,.2f}")
        print(
            f"{'Withdrawals':<12}: "
            f"{self._withdrawals_this_month}/{self._withdrawal_limit} used this month"
        )
        print(f"{'Interest':<12}: {self._interest_rate * 100:.1f}% monthly")
        print("-" * 30)


class InvestmentAccount(Account):
    """
    Investment account with a minimum balance requirement and variable returns.
    """

    _PREFIX = "INV"
    DEFAULT_MINIMUM_BALANCE = 1000.0

    def __init__(self, owner: str, opening_balance: float,
                 minimum_balance: float = DEFAULT_MINIMUM_BALANCE):
        if opening_balance < minimum_balance:
            raise InvalidAmountError(
                f"Opening balance (${opening_balance:,.2f}) must be at least "
                f"the minimum balance (${minimum_balance:,.2f})."
            )
        super().__init__(owner, opening_balance)
        self._minimum_balance = minimum_balance

    @property
    def minimum_balance(self) -> float:
        return self._minimum_balance

    def withdraw(self, amount: float) -> None:
        self._validate_positive_amount(amount, "Withdrawal amount")
        if self._balance - amount < self._minimum_balance:
            raise MinimumBalanceError(
                f"Withdrawal would drop balance below the minimum required "
                f"(${self._minimum_balance:,.2f}). "
                f"Current balance: ${self._balance:,.2f}, "
                f"Max withdrawable: ${max(0.0, self._balance - self._minimum_balance):,.2f}."
            )
        self._balance -= amount
        print(f"Withdrew ${amount:,.2f}. New balance: ${self._balance:,.2f}")

    def apply_return(self, rate: float) -> None:
        """Apply a variable return rate (positive or negative) to the balance."""
        if not isinstance(rate, (int, float)):
            raise InvalidAmountError("Return rate must be a number.")
        gain = self._balance * rate
        self._balance += gain
        direction = "gain" if gain >= 0 else "loss"
        print(
            f"Applied {rate * 100:.2f}% return ({direction} of ${abs(gain):,.2f}). "
            f"New balance: ${self._balance:,.2f}"
        )

    def display_details(self) -> None:
        print("-" * 30)
        print("Account Details")
        print("-" * 30)
        print(f"{'Owner':<12}: {self._owner}")
        print(f"{'Account #':<12}: {self._account_number}")
        print(f"{'Type':<12}: Investment")
        print(f"{'Balance':<12}: ${self._balance:,.2f}")
        print(f"{'Min Balance':<12}: ${self._minimum_balance:,.2f}")
        print("-" * 30)


class Bank:
    """Manages a collection of accounts."""

    def __init__(self, name: str = "PyBank"):
        self._name = name
        self._accounts: dict[str, Account] = {}

    def open_account(self, account: Account) -> Account:
        self._accounts[account.account_number] = account
        return account

    def get_account(self, account_number: str) -> Account:
        account = self._accounts.get(account_number)
        if account is None:
            raise AccountNotFoundError(
                f"No account found with number '{account_number}'."
            )
        return account

    def list_accounts(self) -> None:
        if not self._accounts:
            print("No accounts on file.")
            return
        print("-" * 50)
        print(f"{'#':<6} {'Owner':<20} {'Type':<12} {'Balance':>10}")
        print("-" * 50)
        for acct in self._accounts.values():
            type_name = acct.__class__.__name__.replace("Account", "")
            print(
                f"{acct.account_number:<6}  "
                f"{acct.owner:<20} "
                f"{type_name:<12} "
                f"${acct.balance:>9,.2f}"
            )
        print("-" * 50)


def prompt_float(prompt: str) -> float:
    """Prompt for a float, retrying on bad input."""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("  Please enter a valid number.")


def prompt_int(prompt: str, valid: list[int] | None = None) -> int:
    """Prompt for an integer, optionally validating against a list of choices."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if valid is not None and value not in valid:
                print(f"  Please enter one of: {valid}")
                continue
            return value
        except ValueError:
            print("  Please enter a whole number.")


def menu_checking(account: CheckingAccount) -> None:
    while True:
        print()
        print(f"Account: {account.owner} ({account.account_number})")
        print("[1] Deposit")
        print("[2] Withdraw")
        print("[3] View Details")
        print("[4] Back to Main Menu")
        choice = prompt_int("> ", valid=[1, 2, 3, 4])

        if choice == 1:
            amount = prompt_float("Deposit amount: ")
            try:
                account.deposit(amount)
            except BankingError as e:
                print(f"Error: {e}")

        elif choice == 2:
            amount = prompt_float("Withdrawal amount: ")
            try:
                account.withdraw(amount)
            except BankingError as e:
                print(f"Error: {e}")

        elif choice == 3:
            account.display_details()

        elif choice == 4:
            break


def menu_savings(account: SavingsAccount) -> None:
    while True:
        print()
        print(f"Account: {account.owner} ({account.account_number})")
        print("[1] Deposit")
        print("[2] Withdraw")
        print("[3] Apply Monthly Interest")
        print("[4] View Details")
        print("[5] Back to Main Menu")
        choice = prompt_int("> ", valid=[1, 2, 3, 4, 5])

        if choice == 1:
            amount = prompt_float("Deposit amount: ")
            try:
                account.deposit(amount)
            except BankingError as e:
                print(f"Error: {e}")

        elif choice == 2:
            amount = prompt_float("Withdrawal amount: ")
            try:
                account.withdraw(amount)
            except BankingError as e:
                print(f"Error: {e}")

        elif choice == 3:
            try:
                account.apply_monthly_interest()
            except BankingError as e:
                print(f"Error: {e}")

        elif choice == 4:
            account.display_details()

        elif choice == 5:
            break


def menu_investment(account: InvestmentAccount) -> None:
    while True:
        print()
        print(f"Account: {account.owner} ({account.account_number})")
        print("[1] Deposit")
        print("[2] Withdraw")
        print("[3] Apply Return Rate")
        print("[4] View Details")
        print("[5] Back to Main Menu")
        choice = prompt_int("> ", valid=[1, 2, 3, 4, 5])

        if choice == 1:
            amount = prompt_float("Deposit amount: ")
            try:
                account.deposit(amount)
            except BankingError as e:
                print(f"Error: {e}")

        elif choice == 2:
            amount = prompt_float("Withdrawal amount: ")
            try:
                account.withdraw(amount)
            except BankingError as e:
                print(f"Error: {e}")

        elif choice == 3:
            rate_pct = prompt_float("Return rate (%, e.g. 5 for 5%, -2 for -2%): ")
            try:
                account.apply_return(rate_pct / 100)
            except BankingError as e:
                print(f"Error: {e}")

        elif choice == 4:
            account.display_details()

        elif choice == 5:
            break


def open_new_account(bank: Bank) -> None:
    print()
    print("Account type:")
    print("[1] Checking")
    print("[2] Savings")
    print("[3] Investment")
    acct_type = prompt_int("> ", valid=[1, 2, 3])

    owner = input("Owner name: ").strip()
    if not owner:
        print("Owner name cannot be empty.")
        return

    opening_balance = prompt_float("Opening balance: ")

    try:
        if acct_type == 1:
            overdraft = prompt_float(
                f"Overdraft limit (press Enter for ${CheckingAccount.DEFAULT_OVERDRAFT_LIMIT:.0f}): "
                if False else  # simplify: always prompt
                "Overdraft limit (default 500): "
            )
            account = CheckingAccount(owner, opening_balance, overdraft)

        elif acct_type == 2:
            account = SavingsAccount(owner, opening_balance)

        else:
            min_bal = prompt_float(
                f"Minimum balance requirement (default {InvestmentAccount.DEFAULT_MINIMUM_BALANCE:.0f}): "
            )
            account = InvestmentAccount(owner, opening_balance, min_bal)

        bank.open_account(account)
        type_name = account.__class__.__name__.replace("Account", " Account")
        print(f"\n{type_name} opened for {owner}.")
        print(f"   Account #: {account.account_number}  |  Balance: ${account.balance:,.2f}")

    except BankingError as e:
        print(f"Error opening account: {e}")


def select_account(bank: Bank) -> None:
    account_number = input("Enter account number: ").strip().upper()
    try:
        account = bank.get_account(account_number)
    except AccountNotFoundError as e:
        print(f"Error: {e}")
        return

    print(f"\nAccount selected: {account.owner} ({account.account_number})")

    if isinstance(account, CheckingAccount):
        menu_checking(account)
    elif isinstance(account, SavingsAccount):
        menu_savings(account)
    elif isinstance(account, InvestmentAccount):
        menu_investment(account)
    else:
        print("Unknown account type — basic operations only.")


def main() -> None:
    bank = Bank("PyBank")

    print("=" * 30)
    print("   Welcome to PyBank CLI")
    print("=" * 30)

    while True:
        print()
        print("[1] Open a new account")
        print("[2] Select an account")
        print("[3] List all accounts")
        print("[4] Quit")
        choice = prompt_int("> ", valid=[1, 2, 3, 4])

        if choice == 1:
            open_new_account(bank)

        elif choice == 2:
            select_account(bank)

        elif choice == 3:
            bank.list_accounts()

        elif choice == 4:
            print("Goodbye!")
            break

        print("-" * 30)


if __name__ == "__main__":
    main()