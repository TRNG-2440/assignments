from pydantic import BaseModel, Field
from datetime import date

class EntryResponse(BaseModel):
    entry_id: int
    entry_date: date
    entry_title: str
    entry_body: str

class EntryCreate(BaseModel):
    entry_title: str = Field(default="my journal entry", max_length=64)
    entry_body: str = Field(default="", max_length=1000)

class EntryUpdate(BaseModel):
    entry_id: int = Field(gt=0)
    entry_title: str = Field(default="", max_length=64)
    entry_body: str = Field(default="", max_length=1000)