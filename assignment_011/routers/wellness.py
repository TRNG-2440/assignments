from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from models import (
    WellnessCreate,
    WellnessResponse,
    WellnessSummary,
    WellnessUpdate,
    WellnessResponse
)

from storage import write_data, read_data
from auth import verify_api_key

router = APIRouter(
    prefix="/wellness",
    tags=["wellness Tracker"],
    dependencies=[Depends(verify_api_key)]
)

FILE_PATH = "data/wellness_tracker.json"



#Create ENTRY
@router.post("/", response_model=WellnessResponse,
             status_code=201,
             summary="Create a wellness entry",
             description="Creates new daily wellness entry")


def create_entry(payload: WellnessCreate):
    data = read_data(FILE_PATH) or []

    if not data:
        next_id = 1
    else:
        last_id = data[-1]["id"]  
        last_num = int(last_id.split("-")[1])
        next_id = last_num + 1

    new_entry = {
    "id": f"ENT-{next_id}",
    "created_at": datetime.now().isoformat(),
    "date": payload.date.isoformat(),
    "sleep_hours": payload.sleep_hours,
    "water_intake": payload.water_intake,
    "exercise_time": payload.exercise_time,
    "notes": payload.notes
    }
    
    data.append(new_entry)
    write_data(FILE_PATH, data)
    return new_entry


##READ ALL ENTRIES
@router.get("/", response_model=list[WellnessResponse],
            summary="Get all wellness entries",
            description="Returns all wellness entries")

def get_all_entries():
    return read_data(FILE_PATH) or []

##GET ENTRY BY ID
@router.get("/entry/{entry_id}", response_model=WellnessResponse,
            summary="Get wellness entry by ID",
            description="Returns a wellness entry by ID")

def get_entry(entry_id: str):
    data =  read_data(FILE_PATH)

    for entry in data:
        if entry["id"] == entry_id:
            return entry

    raise HTTPException(
        status_code=404,
        detail=f"Entry {entry_id} not found",
    )

## UPDATE ENTRY

@router.put(
    "/{entry_id}",
    response_model=WellnessResponse,
    summary="Update wellness entry",
    description="Fully updates an existing wellness entry."
)
def update_entry(entry_id: str, payload: WellnessUpdate):
    data = read_data(FILE_PATH)

    for index, entry in enumerate(data):
        if entry["id"] == entry_id:

            updated_entry = {
                "id": entry["id"],
                "created_at": entry["created_at"],
                "date": payload.date.isoformat(),
                "sleep_hours": payload.sleep_hours,
                "water_intake": payload.water_intake,
                "exercise_time": payload.exercise_time,
                "notes": payload.notes
            }

            data[index] = updated_entry
            write_data(FILE_PATH, data)

            return updated_entry

    raise HTTPException(
        status_code=404,
        detail=f"Entry {entry_id} not found",
    )

## DELETE ENTRY
@router.delete(
    "/{entry_id}",
    summary="Delete wellness entry",
    description="Deletes an existing wellness entry.")

def delete_entry(entry_id: str):
    data = read_data(FILE_PATH)

    for index, entry in enumerate(data):
        if entry["id"] == entry_id:
            deleted = data.pop(index)
            write_data(FILE_PATH, data)
            return {
                "message": "Entry deleted successfully",
                "deleted_id": deleted["id"]
            }

    raise HTTPException(
        status_code=404,
        detail=f"Entry {entry_id} not found",
    )

##SUMMARY
@router.get("/summary", response_model=WellnessSummary,
            summary="Get wellness Summary",
            description="Returns a wellness Summary")

def get_summary():
    data = read_data(FILE_PATH)

    if not data:
        return {
            "total_entries": 0,
            "average_sleep": 0,
            "average_water_intake": 0,
            "average_exercise": 0
        }
    
    total_entries = len(data)
    average_sleep = sum(entry["sleep_hours"] for entry in data) / total_entries
    average_water = sum(entry["water_intake"] for entry in data) / total_entries
    average_exercise = sum(entry["exercise_time"] for entry in data) / total_entries

    return {
        "total_entries": total_entries,
        "average_sleep": round(average_sleep, 2), 
        "average_water_intake": round(average_water, 2), 
        "average_exercise": round(average_exercise, 2)
    }