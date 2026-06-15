from account import Account
from exceptions import MinimumBalanceError


class InvestmentAccount(Account):

    def __init__(self, owner, balance):
        super().__init__(owner, balance)

        self.account_number = f"INV-{Account.next_id:05}"
        Account.next_id += 1

        self.minimum_balance = 1000

    def withdraw(self, amount):

        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if self.balance - amount < self.minimum_balance:
            raise MinimumBalanceError(
                f"Cannot drop below ${self.minimum_balance:.2f}"
            )

        self.balance -= amount

    def apply_return(self, rate):
        self.balance += self.balance * rate

    def get_details(self):
        return (
            f"Type: Investment\n"
            f"Owner: {self.owner}\n"
            f"Account #: {self.account_number}\n"
            f"Balance: ${self.balance:.2f}\n"
            f"Minimum Balance: ${self.minimum_balance:.2f}"
        )