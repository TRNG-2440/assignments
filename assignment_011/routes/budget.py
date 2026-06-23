from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from services.budget import upsert_budget_goals, create_user_budget
from models.budget import BudgetGoalDAO, BudgetResponse


router = APIRouter()


@router.post(
    "/budget", status_code=status.HTTP_201_CREATED, response_model=BudgetResponse
)
def create_budget(
    budget_response: Annotated[BudgetResponse, Depends(create_user_budget)],
) -> BudgetResponse:
    return budget_response


@router.put(
    "/budget/{budget_id}/goals",
    status_code=status.HTTP_200_OK,
    response_model=List[BudgetGoalDAO],
)
def upsert_goals(
    goals: Annotated[List[BudgetGoalDAO], Depends(upsert_budget_goals)],
) -> List[BudgetGoalDAO]:
    return goals
