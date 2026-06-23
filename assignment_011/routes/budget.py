from typing import Annotated, List

from fastapi import APIRouter, Depends, Response, status

from services.budget import (
    delete_user_budget,
    get_user_budget,
    get_user_budgets,
    upsert_budget_goals,
    create_user_budget,
)
from models.budget import BudgetGoalDAO, BudgetResponse, BudgetUpsertResponse


router = APIRouter()


@router.post(
    "/budget", status_code=status.HTTP_201_CREATED, response_model=BudgetUpsertResponse
)
def create_budget(
    budget_response: Annotated[BudgetUpsertResponse, Depends(create_user_budget)],
) -> BudgetUpsertResponse:
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


@router.get(
    "/budget/{id}", status_code=status.HTTP_200_OK, response_model=BudgetResponse
)
def get_budget(
    budget: Annotated[BudgetResponse, Depends(get_user_budget)],
) -> BudgetResponse:
    return budget


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=List[BudgetUpsertResponse]
)
def get_budgets(
    budgets: Annotated[List[BudgetUpsertResponse], Depends(get_user_budgets)],
) -> List[BudgetUpsertResponse]:
    return budgets


@router.delete(
    "/budget/{budget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_budget(result=Depends(delete_user_budget)) -> Response:
    return result
