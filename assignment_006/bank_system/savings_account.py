from account import Account
from exceptions import WithdrawalLimitError


class SavingsAccount(Account):
    def __init__(self, owner, balance):
        super().__init__(owner, balance)

        self.account_number = f"SAV-{Account.next_id:05}"
        Account.next_id += 1

        self.interest_rate = 0.025
        self.withdrawals_used = 0
        self.withdrawal_limit = 3

    def withdraw(self, amount):

        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if self.withdrawals_used >= self.withdrawal_limit:
            raise WithdrawalLimitError(
                "Monthly withdrawal limit reached."
            )

        if amount > self.balance:
            raise ValueError("Insufficient funds.")

        self.balance -= amount
        self.withdrawals_used += 1

    def apply_interest(self):
        self.balance += self.balance * self.interest_rate

    def get_details(self):
        return (
            f"Type: Savings\n"
            f"Owner: {self.owner}\n"
            f"Account #: {self.account_number}\n"
            f"Balance: ${self.balance:.2f}\n"
            f"Withdrawals: {self.withdrawals_used}/{self.withdrawal_limit}\n"
            f"Interest Rate: {self.interest_rate * 100:.1f}%"
        )
    

    