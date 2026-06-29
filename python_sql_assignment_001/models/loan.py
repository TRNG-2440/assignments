from dataclasses import dataclass
from datetime import date
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class LoanCreate(BaseModel):
    book_id: Annotated[int, Field(description="Id of the book to borrow")]
    member_id: Annotated[int, Field(description="Id of the member who is borrowing")]
    loan_date: Annotated[date, Field(description="Date of borrowing the book")]
    due_date: Annotated[date, Field(description="Date by which book must be returned")]
    return_date: Annotated[
        Optional[date], Field(description="Date when book was actually returned")
    ]


class LoanResponse(BaseModel):
    loan_id: Annotated[int, Field(description="Id of the loan")]
    book_id: Annotated[int, Field(description="Id of the book to borrow")]
    member_id: Annotated[int, Field(description="Id of the member who is borrowing")]
    loan_date: Annotated[date, Field(description="Date of borrowing the book")]
    due_date: Annotated[date, Field(description="Date by which book must be returned")]
    return_date: Annotated[
        Optional[date], Field(description="Date when book was actually returned")
    ]


@dataclass
class Loan:
    loan_id: int
    book_id: int
    member_id: int
    loan_date: date
    due_date: date
    return_date: date
