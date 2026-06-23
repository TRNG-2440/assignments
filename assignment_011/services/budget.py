from typing import Annotated, Dict, List, Type, cast

from fastapi import Depends

from services.auth import verify_credentials
from models.users import UserResponse
from repository.budget import BudgetRepository, BudgetGoalsRepository
from exceptions import ResourceNotFoundError, UnauthorizedAccessError
from models.budget import (
    BaseGoalDAO,
    BudgetCreate,
    BudgetDAO,
    BudgetGoalCreate,
    BudgetGoalDAO,
    BudgetResponse,
    ExpenseGoalDAO,
    GoalType,
)

GOAL_DAO_MAP: Dict[GoalType, Type[BaseGoalDAO]] = {
    GoalType.EXPENSE: ExpenseGoalDAO,
}


def create_user_budget(
    budget: BudgetCreate,
    user: Annotated[UserResponse, Depends(verify_credentials)],
    budget_repo: Annotated[BudgetRepository, Depends()],
) -> BudgetResponse:
    new_budget: BudgetDAO = _create_record(budget, user.id)
    budget_repo.create_budget(new_budget)
    return BudgetResponse.model_validate(new_budget.model_dump())


def _create_record(budget: BudgetCreate, user_id: str) -> BudgetDAO:
    budget_data = budget.model_dump()
    budget_data["user_id"] = user_id
    return BudgetDAO.model_validate(budget_data)


def upsert_budget_goals(
    goals: List[BudgetGoalCreate],
    budget_id: str,
    user: Annotated[UserResponse, Depends(verify_credentials)],
    budget_repo: Annotated[BudgetRepository, Depends()],
    budget_goals_repo: Annotated[BudgetGoalsRepository, Depends()],
) -> List[BudgetGoalDAO]:
    # Valid budget check
    if not budget_repo.has_budget(budget_id):
        raise ResourceNotFoundError("budget", budget_id)
    # Valid budget_id for user check
    if not budget_repo.is_user_budget_owner(user.id, budget_id):
        raise UnauthorizedAccessError(user.id, "budget", budget_id)

    # Upsert expense goals
    goals_dto: List[BudgetGoalDAO] = _create_budget_goal_records(goals, budget_id)
    return budget_goals_repo.upsert_budget_goals(goals_dto)


def _create_budget_goal_records(
    goals: List[BudgetGoalCreate], budget_id: str
) -> List[BudgetGoalDAO]:
    return [_create_budget_goal_record(goal, budget_id) for goal in goals]


def _create_budget_goal_record(goal: BudgetGoalCreate, budget_id: str) -> BudgetGoalDAO:
    goal_dict = goal.model_dump()
    goal_dict["budget_id"] = budget_id

    goal_type = goal.type
    dao_class = GOAL_DAO_MAP.get(goal_type)

    if not dao_class:
        raise ValueError(f"Unsupported goal type: {goal_type}")
    return cast(BudgetGoalDAO, dao_class(**goal_dict))
