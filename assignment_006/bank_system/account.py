class Account:

    next_id = 1

    def __init__(self, owner, balance):
        
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        self.balance += amount
    def get_details(self):
        return (
            f"Owner: {self.owner}\n"
            f"Account #: {self.account_number}\n"
            f"Balance: ${self.balance:.2f}"
        )