class Bank:

    def __init__(self):
        self.accounts = {}

    def open_account(self, account):
        self.accounts[account.account_number] = account

    def find_account(self, account_number):
        return self.accounts.get(account_number)

    def list_accounts(self):

        if not self.accounts:
            print("No accounts found.")
            return

        for account in self.accounts.values():
            print(
                f"Account Type: {type(account).__name__} | "
                f"Account Owner: {account.owner} | "
                f"Account Number: {account.account_number} | "
                f"Account Balance: ${account.balance:.2f}"
            )
    