class BankingError(Exception):
    pass


class OverdraftExceededError(BankingError):
    pass


class WithdrawalLimitError(BankingError):
    pass


class MinimumBalanceError(BankingError):
    pass