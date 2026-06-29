from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from models.loan import LoanCreate, LoanResponse
from dependencies import get_loan_service
from services import LoanService


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=List[LoanResponse])
def get_all(
    loan_service: Annotated[LoanService, Depends(get_loan_service)],
) -> List[LoanResponse]:
    return loan_service.get_all()


@router.get(
    "/active", status_code=status.HTTP_200_OK, response_model=List[LoanResponse]
)
def get_active_loans(
    loan_service: Annotated[LoanService, Depends(get_loan_service)],
) -> List[LoanResponse]:
    return loan_service.get_active_loans()


@router.get("/{loan_id}", status_code=status.HTTP_200_OK, response_model=LoanResponse)
def get_by_id(
    loan_id: int,
    loan_service: Annotated[LoanService, Depends(get_loan_service)],
) -> LoanResponse:
    return loan_service.get_by_id(loan_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=LoanResponse)
def create(
    loan: LoanCreate,
    loan_service: Annotated[LoanService, Depends(get_loan_service)],
) -> LoanResponse:
    return loan_service.create(loan)


@router.patch("/{loan_id}", status_code=status.HTTP_200_OK, response_model=LoanResponse)
def return_book(
    loan_id: int,
    loan_service: Annotated[LoanService, Depends(get_loan_service)],
) -> LoanResponse:
    return loan_service.return_book(loan_id)


@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(
    loan_id: int,
    loan_service: Annotated[LoanService, Depends(get_loan_service)],
) -> None:
    return loan_service.delete_by_id(loan_id)
