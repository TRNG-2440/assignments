from account import Account
from exceptions import OverdraftExceededError


class CheckingAccount(Account):

    def __init__(self, owner, balance):
        super().__init__(owner, balance)

        self.account_number = f"CHK-{Account.next_id:05}"
        Account.next_id += 1

        self.overdraft_limit = 100

    def withdraw(self, amount):

        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if self.balance - amount < -self.overdraft_limit:
            raise OverdraftExceededError(
                "Overdraft limit exceeded."
            )

        self.balance -= amount

    def get_details(self):
        return (
            f"Type: Checking\n"
            f"Owner: {self.owner}\n"
            f"Account #: {self.account_number}\n"
            f"Balance: ${self.balance:.2f}\n"
            f"Overdraft Limit: ${self.overdraft_limit:.2f}"
        )
