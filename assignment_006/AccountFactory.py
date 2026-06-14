"""
AccountFactory.py

Provides a factory for creating concrete `Account` subclass instances
based on an `AccountType`, without the caller needing to know which
concrete class corresponds to which type.
"""

from typing import Any

from Account import Account, AccountType
from CheckingAccount import CheckingAccount
from InvestmentAccount import InvestmentAccount
from SavingsAccount import SavingsAccount
from custom_exceptions import UnknownAccountTypeError


class AccountFactory:
    """Factory class for instantiating `Account` subclasses by type."""

    # Maps each AccountType to the concrete Account subclass that implements it.
    _registry = {
        AccountType.CHECKING: CheckingAccount,
        AccountType.SAVINGS: SavingsAccount,
        AccountType.INVESTMENT: InvestmentAccount,
    }

    @classmethod
    def create_account(cls, account_type: AccountType, **kwargs: Any) -> Account:
        """Create and return a new account instance of the given type.

        Args:
            account_type: The type of account to create.
            **kwargs: Additional keyword arguments forwarded to the
                concrete account class's constructor (e.g.
                `customer_name`, `opening_balance`, `roi`).

        Returns:
            A new instance of the `Account` subclass corresponding to
            `account_type`.

        Raises:
            UnknownAccountTypeError: If `account_type` has no registered
                account class.
        """
        # Look up the concrete class registered for this account type.
        account_class = cls._registry.get(account_type)
        if not account_class:
            raise UnknownAccountTypeError(account_type)
        # Instantiate the concrete class, passing the account type along
        # with any other constructor arguments.
        return account_class(account_type=account_type, **kwargs)
