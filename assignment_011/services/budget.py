from typing import Annotated

from fastapi import Depends

from services.auth import verify_credentials
from models.users import UserResponse
from repository.budget import BudgetRepository
from models.budget import BudgetCreate, BudgetDAO, BudgetResponse


def create_user_budget(
    budget: BudgetCreate,
    user: Annotated[UserResponse, Depends(verify_credentials)],
    budget_repo: Annotated[BudgetRepository, Depends()],
) -> BudgetResponse:
    new_budget: BudgetDAO = create_record(budget, user.id)
    budget_repo.create_budget(new_budget)
    return BudgetResponse.model_validate(new_budget.model_dump())


def create_record(budget: BudgetCreate, user_id: str) -> BudgetDAO:
    budget_data = budget.model_dump()
    budget_data["user_id"] = user_id
    return BudgetDAO.model_validate(budget_data)
