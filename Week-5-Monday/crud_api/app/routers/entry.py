from fastapi import APIRouter, HTTPException
from ..models import EntryResponse, EntryCreate, EntryUpdate
from datetime import date

router = APIRouter(
    prefix="/entry",
    tags=["entry"],
    responses={404:{"description": "entry not found"}}
)

_THE_DB = {}
_ENTRY_ID = 1

def get_or_except(entry_id: int):
    try:
        entry = _THE_DB[entry_id]
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"no entry found at {entry_id}")

    return entry

# get by id
@router.get(
    path="/{entry_id}",
    response_model=EntryResponse,
    status_code=200,
    tags=["get"],
    summary="get all entries",
    description="return a list of EntryResponse objects for every response in DB"
)
def get_entry(entry_id: int):
    return get_or_except(entry_id)

# list all
@router.get(
    path="", 
    response_model=list[EntryResponse],
    status_code=200,
    tags=["get"],
    summary="get all entries",
    description="return a list of EntryResponse objects for every response in DB"
)
def list_all():
    return [ent for ent in _THE_DB.values()]

# create
@router.post(
    path="", 
    response_model=EntryResponse, 
    status_code=201, 
    tags=["entry", "create"],
    summary="create a new journal entry",
    description="create journal entry using post method with auto incrementing id and today as entry date"
)
def create(payload: EntryCreate):
    global _ENTRY_ID
    record = {
        "entry_id": _ENTRY_ID,
        "entry_date": date.today(),
        **payload.model_dump()
    }
    _THE_DB[_ENTRY_ID] = record
    _ENTRY_ID += 1
    return record


# replace?
@router.put(
        path="/{entry_id}",
        response_model=EntryResponse,
        status_code=200,
        tags=["replace", "update"]
)
def replace(payload: EntryUpdate):
    entry = get_or_except(payload.entry_id)
    entry["entry_title"] = payload.entry_title if payload.entry_title else entry["entry_title"]
    entry["entry_body"] = payload.entry_body if payload.entry_body else entry["entry_body"]
    _THE_DB[payload.entry_id] = entry
    return entry
    
# delete
@router.delete(
    path="/{entry_id}"
)
def delete(entry_id: int):
    get_or_except(entry_id)
    _THE_DB.pop(entry_id)
    return None