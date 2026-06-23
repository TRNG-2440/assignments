from typing import Annotated, List

from fastapi import APIRouter, Response, status, Depends

from services.transaction import create_trnxs, delete_trnx, get_trnxs
from models.transaction import TransactionResponse


router = APIRouter()


@router.post(
    "/transaction",
    status_code=status.HTTP_201_CREATED,
    response_model=List[TransactionResponse],
)
def create_transactions(
    transactions: Annotated[List[TransactionResponse], Depends(create_trnxs)],
) -> List[TransactionResponse]:
    return transactions


@router.delete(
    "/transaction/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
def delete_transaction(result=Depends(delete_trnx)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/transaction",
    status_code=status.HTTP_200_OK,
    response_model=List[TransactionResponse],
)
def get_transactions(
    transactions: Annotated[List[TransactionResponse], Depends(get_trnxs)],
) -> List[TransactionResponse]:
    return transactions
