from typing import Annotated, Dict, List, Type, cast

from fastapi import Depends

from exceptions import ResourceNotFoundError, UnauthorizedAccessError
from models.categories import BudgetCategory
from repository.transaction import TransactionRepository
from services.auth import verify_credentials
from models.users import UserResponse
from models.transaction import (
    BaseTransactionDAO,
    BaseTransactionResponse,
    ExpenseTransactionDAO,
    ExpenseTransactionResponse,
    IncomeTransactionDAO,
    IncomeTransactionResponse,
    TransactionCreate,
    TransactionDAO,
    TransactionFilterParams,
    TransactionResponse,
)

TRANSACTION_DAO_MAP: Dict[BudgetCategory, Type[BaseTransactionDAO]] = {
    BudgetCategory.INCOME: IncomeTransactionDAO,
    BudgetCategory.EXPENSE: ExpenseTransactionDAO,
}

TRANSACTION_RESPONSE_MAP: Dict[BudgetCategory, Type[BaseTransactionResponse]] = {
    BudgetCategory.INCOME: IncomeTransactionResponse,
    BudgetCategory.EXPENSE: ExpenseTransactionResponse,
}


def create_trnxs(
    transactions: List[TransactionCreate],
    user: Annotated[UserResponse, Depends(verify_credentials)],
    trnx_repo: Annotated[TransactionRepository, Depends()],
) -> List[TransactionResponse]:
    trnxs_dto: List[TransactionDAO] = _create_records(transactions, user.id)
    trnx_repo.create_transactions(trnxs_dto)
    return _create_response_records(trnxs_dto)


def get_trnxs(
    params: Annotated[TransactionFilterParams, Depends()],
    user: Annotated[UserResponse, Depends(verify_credentials)],
    trnx_repo: Annotated[TransactionRepository, Depends()],
) -> List[TransactionResponse]:
    trnxs_dto: List[TransactionDAO] = trnx_repo.get_transactions(user.id, params)
    return _create_response_records(trnxs_dto)


def delete_trnx(
    id: str,
    user: Annotated[UserResponse, Depends(verify_credentials)],
    trnx_repo: Annotated[TransactionRepository, Depends()],
) -> None:
    # check transaction exists
    if not trnx_repo.is_trnx(id):
        return  # delete is idempotent
    # check trnx belongs to user
    if not trnx_repo.is_trnx_owner_user(user.id, id):
        raise UnauthorizedAccessError(user.id, "transaction", id)
    trnx_repo.delete_trnx(id)


def _create_records(
    transactions: List[TransactionCreate], user_id: str
) -> List[TransactionDAO]:
    return [_create_record(trnx, user_id) for trnx in transactions]


def create_trnx_response_records(
    transactions: List[TransactionDAO],
) -> List[TransactionResponse]:
    return _create_response_records(transactions)


def _create_response_records(
    transactions: List[TransactionDAO],
) -> List[TransactionResponse]:
    return [_create_response_record(trnx) for trnx in transactions]


def _create_record(transaction: TransactionCreate, user_id: str) -> TransactionDAO:
    trnx_dict = transaction.model_dump()
    trnx_dict["user_id"] = user_id

    trnx_budget_type = transaction.budget_category
    dao_class = TRANSACTION_DAO_MAP.get(trnx_budget_type)
    if not dao_class:
        raise ValueError(f"Unsupported transaction budget type: {trnx_budget_type}")
    return cast(TransactionDAO, dao_class(**trnx_dict))


def _create_response_record(transaction: TransactionDAO) -> TransactionResponse:
    trnx_dict = transaction.model_dump()

    trnx_budget_type = transaction.budget_category
    dao_class = TRANSACTION_RESPONSE_MAP.get(trnx_budget_type)
    if not dao_class:
        raise ValueError(f"Unsupported transaction budget type: {trnx_budget_type}")
    return cast(TransactionResponse, dao_class(**trnx_dict))
