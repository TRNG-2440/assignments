from datetime import date, datetime
from typing import Annotated, Literal, Union
from uuid import uuid4

from fastapi import Query
from pydantic import BaseModel, Field

from models.categories import BudgetCategory, ExpenseCategory


class BaseTransactionCreate(BaseModel):
    amount: Annotated[float, Field(gt=0, description="Transaction amount")]
    transaction_date: Annotated[date, Field(description="Transaction date")]
    description: Annotated[str, Field(description="Description of the transaction")]


class IncomeTransactionCreate(BaseTransactionCreate):
    budget_category: Literal[BudgetCategory.INCOME] = BudgetCategory.INCOME
    budget_subcategory: None = None  # Strictly forbids subcategories for income


class ExpenseTransactionCreate(BaseTransactionCreate):
    budget_category: Literal[BudgetCategory.EXPENSE] = BudgetCategory.EXPENSE
    budget_subcategory: ExpenseCategory  # Strictly REQUIRED for expenses


TransactionCreate = Annotated[
    Union[IncomeTransactionCreate, ExpenseTransactionCreate],
    Field(discriminator="budget_category"),
]


class BaseTransactionDAO(BaseTransactionCreate):
    id: str = Field(
        default_factory=lambda: uuid4().hex, description="Id of transaction"
    )
    user_id: Annotated[str, Field(description="Id of user")]
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp at which transaction is created",
    )
    last_updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp at which transaction is last updated",
    )


class IncomeTransactionDAO(BaseTransactionDAO):
    budget_category: Literal[BudgetCategory.INCOME] = BudgetCategory.INCOME
    budget_subcategory: None = None  # Strictly forbids subcategories for income


class ExpenseTransactionDAO(BaseTransactionDAO):
    budget_category: Literal[BudgetCategory.EXPENSE] = BudgetCategory.EXPENSE
    budget_subcategory: ExpenseCategory  # Strictly REQUIRED for expenses


TransactionDAO = Annotated[
    Union[IncomeTransactionDAO, ExpenseTransactionDAO],
    Field(discriminator="budget_category"),
]


class BaseTransactionResponse(BaseTransactionCreate):
    id: str = Field(
        default_factory=lambda: uuid4().hex, description="Id of transaction"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp at which transaction is created",
    )
    last_updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp at which transaction is last updated",
    )


class IncomeTransactionResponse(BaseTransactionResponse):
    budget_category: Literal[BudgetCategory.INCOME] = BudgetCategory.INCOME
    budget_subcategory: None = None  # Strictly forbids subcategories for income


class ExpenseTransactionResponse(BaseTransactionResponse):
    budget_category: Literal[BudgetCategory.EXPENSE] = BudgetCategory.EXPENSE
    budget_subcategory: ExpenseCategory  # Strictly REQUIRED for expenses


TransactionResponse = Annotated[
    Union[IncomeTransactionResponse, ExpenseTransactionResponse],
    Field(discriminator="budget_category"),
]


class TransactionFilterParams(BaseModel):
    start_date: Annotated[
        date, Query(description="Start date of transaction(inclusive)")
    ] = date(1970, 1, 1)
    end_date: Annotated[
        date, Query(description="End date of transaction(inclusive)")
    ] = date.today()
