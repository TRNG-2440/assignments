from dataclasses import dataclass
from datetime import date
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class MemberCreate(BaseModel):
    name: Annotated[str, Field(description="Name of the member")]
    email: Annotated[EmailStr, Field(description="Email of the member")]
    join_date: Annotated[
        date, Field(default_factory=date.today, description="Joining date")
    ]


class MemberResponse(BaseModel):
    member_id: Annotated[int, Field(description="Id of the member")]
    name: Annotated[str, Field(description="Name of the member")]
    email: Annotated[EmailStr, Field(description="Email of the member")]
    join_date: Annotated[
        date, Field(default_factory=date.today, description="Joining date")
    ]


@dataclass
class Member:
    name: str
    email: str
    join_date: date
    member_id: int = -1
