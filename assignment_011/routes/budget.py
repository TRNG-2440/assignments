from typing import Annotated

from fastapi import APIRouter, Depends, status

from services.budget import create_user_budget
from models.budget import BudgetResponse


router = APIRouter()


@router.post("/budget", status_code=status.HTTP_201_CREATED)
def create_budget(
    budget_response: Annotated[BudgetResponse, Depends(create_user_budget)],
) -> BudgetResponse:
    return budget_response
