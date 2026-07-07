from datetime import time
from typing import Optional
from uuid import UUID

from pydantic import Field, BaseModel


class RacecarCreate(BaseModel):
    team: str = Field(min_length=2, max_length=50)
    fuel: float = Field(gt=0)
    disqualified: bool

class Racecar(BaseModel):
    id: int
    team: str = Field(min_length=2, max_length=50)
    fuel: float = Field(gt=0)
    disqualified: bool
