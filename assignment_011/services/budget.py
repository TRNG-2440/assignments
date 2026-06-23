from typing import Annotated, Dict, List, Type, cast

from fastapi import Depends

from models.categories import BudgetCategory, ExpenseCategory
from models.transaction import TransactionResponse
from repository.transaction import TransactionRepository
from services.transaction import create_trnx_response_records
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
    BudgetSummaryInsights,
    BudgetUpsertResponse,
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
) -> BudgetUpsertResponse:
    new_budget: BudgetDAO = _create_record(budget, user.id)
    budget_repo.create_budget(new_budget)
    return BudgetUpsertResponse.model_validate(new_budget.model_dump())


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


def get_user_budget(
    id: str,
    user: Annotated[UserResponse, Depends(verify_credentials)],
    budget_repo: Annotated[BudgetRepository, Depends()],
    budget_goals_repo: Annotated[BudgetGoalsRepository, Depends()],
    trnx_repo: Annotated[TransactionRepository, Depends()],
) -> BudgetResponse:
    # Valid budget check
    if not budget_repo.has_budget(id):
        raise ResourceNotFoundError("budget", id)
    # Valid budget_id for user check
    if not budget_repo.is_user_budget_owner(user.id, id):
        raise UnauthorizedAccessError(user.id, "budget", id)
    budget: BudgetUpsertResponse = BudgetUpsertResponse.model_validate(
        budget_repo.get_budget(user.id, id).model_dump()
    )
    budget_goals: List[BudgetGoalDAO] = budget_goals_repo.get_budget_goals(id)
    transactions: List[TransactionResponse] = create_trnx_response_records(
        trnx_repo.get_budget_transactions(user.id, budget.start_date, budget.end_date)
    )
    summary_insights: BudgetSummaryInsights = _calculate_summary_insights(
        budget_goals, transactions
    )
    return _create_budget_response_record(
        budget, budget_goals, transactions, summary_insights
    )


def get_user_budgets(
    user: Annotated[UserResponse, Depends(verify_credentials)],
    budget_repo: Annotated[BudgetRepository, Depends()],
) -> List[BudgetUpsertResponse]:
    return _create_budgets_records(budget_repo.get_budgets(user.id))


def _calculate_summary_insights(
    budget_goals: List[BudgetGoalDAO],
    transactions: List[TransactionResponse],
) -> BudgetSummaryInsights:
    total_income = 0.0
    total_expenses = 0.0
    expenses_per_category: Dict[ExpenseCategory, float] = {
        cat: 0.0 for cat in ExpenseCategory
    }

    for trnx in transactions:
        if trnx.budget_category == BudgetCategory.INCOME:
            total_income += trnx.amount
        elif trnx.budget_category == BudgetCategory.EXPENSE:
            total_expenses += trnx.amount
            # Assuming transaction has an 'expense_category' field (e.g., HOUSING, FOOD)
            if hasattr(trnx, "budget_subcategory") and trnx.budget_subcategory:
                expenses_per_category[trnx.budget_subcategory] += trnx.amount

    goal_achieved_or_not: Dict[str, bool] = {}
    for goal in budget_goals:
        if goal.category:
            actual_spent = expenses_per_category.get(goal.category, 0.0)
        else:
            actual_spent = sum(expenses_per_category.values())
        # Goal is achieved if actual spending is less than or equal to the goal target amount
        goal_achieved_or_not[goal.id] = actual_spent <= goal.goal_amount

    response_dict = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_savings_or_deficit": total_income - total_expenses,
        "expenses_per_category": expenses_per_category,
        "goal_achieved_or_not": goal_achieved_or_not,
    }

    return BudgetSummaryInsights.model_validate(response_dict)


def _create_budgets_records(budgets: List[BudgetDAO]) -> List[BudgetUpsertResponse]:
    return [
        BudgetUpsertResponse.model_validate(budget.model_dump()) for budget in budgets
    ]


def _create_budget_response_record(
    budget: BudgetUpsertResponse,
    budget_goals: List[BudgetGoalDAO],
    transactions: List[TransactionResponse],
    summary_insights: BudgetSummaryInsights,
) -> BudgetResponse:
    response_dict = {}
    response_dict["budget"] = budget
    response_dict["goals"] = budget_goals
    response_dict["transactions"] = transactions
    response_dict["summary_insights"] = summary_insights

    return BudgetResponse.model_validate(response_dict)


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
