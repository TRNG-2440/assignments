from fastapi import FastAPI, HTTPException, Depends 
from models import LogEntryCreate, LogEntryResponse, LogEntryUpdate
from typing import Optional
from uuid import uuid4
from datetime import datetime
from storage import read_data, write_data
from auth import check_key_header
import logging

app = FastAPI(
    title="Gardening API", 
    description="a gardening log data", 
    version="0.1.0"
)

log_entry_db = read_data()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# get single
@app.get(
    path="/logentries/{log_entry_id}", 
    response_model=LogEntryResponse,
    status_code=200,
    tags=["log_entry", "get"],
    summary="get a single log entry by id",
    description="gets a log entry by id from the json db. requires authentication. returns record as a LogEntryResponse object",
        responses={
        401: {"description": "Unauthorised — invalid or missing credentials"},
        422: {"description": "Validation error — request body did not match the expected schema"},
    })
def get_log_entry(log_entry_id: str, api_key: str = Depends(check_key_header)):
    for log_entry in log_entry_db:
        if log_entry["id"].strip().lower() == log_entry_id.strip().lower():
            return log_entry
    raise HTTPException(status_code=404, detail=f"log entry with ID {log_entry_id} not found")

# get all
@app.get(
    path="/logentries",
    status_code=200,
    tags=["log_entry", "get"],
    summary="get all log entries",
    description="get all log entries. Optionally filters by activity. requires authentication. returns a list of json objects",
    responses={
        401: {"description": "Unauthorised — invalid or missing credentials"},
        422: {"description": "Validation error — request body did not match the expected schema"},
    })
def get_all_log_entries(activity: Optional[str] = None, api_key: str = Depends(check_key_header)):
    if activity:
        return [entry for entry in log_entry_db if entry["activity"].lower() == activity.lower()]
    return log_entry_db

# create
@app.post(
    path="/logentries",
    response_model=LogEntryResponse,
    status_code=201,
    tags=["log_entry", "create"],
    summary="create log entry",
    description="create a log entry with a type of activity, description and location with id and creation timestamp auto generated. authentication required",
    responses={
        401: {"description": "Unauthorised — invalid or missing credentials"},
        422: {"description": "Validation error — request body did not match the expected schema"},
    })
def create_log_entry(log_entry: LogEntryCreate, api_key: str = Depends(check_key_header)):
    new_log_entry = {
        "id": str(uuid4()),
        "created_at": str(datetime.now()),
        "activity": log_entry.activity.lower(),
        "description": log_entry.description,
        "location" : log_entry.location
    }
    log_entry_db.append(new_log_entry)
    write_data(log_entry_db)
    return new_log_entry

# update
@app.patch(
    path="/logentries/{log_entry_id}",
    response_model=LogEntryResponse,
    status_code=200,
    tags=["log_entry", "update"],
    summary="update a log entry by id",
    description="update activity type, description and location with optional values. authentication required, returns LogEntryResponse object",
    responses={
        401: {"description": "Unauthorised — invalid or missing credentials"},
        422: {"description": "Validation error — request body did not match the expected schema"},
    })
def update_log_entry(log_entry_id: str, log_entry_update: LogEntryUpdate, api_key: str = Depends(check_key_header)):
    for idx, log_entry in enumerate(log_entry_db):
        if log_entry["id"] == log_entry_id.lower():
            updated_fields = log_entry_update.model_dump(exclude_none=True)
            log_entry_db[idx].update(updated_fields)
            write_data(log_entry_db)
            return log_entry
    raise HTTPException(status_code=404, detail=f"Log Entry: {log_entry_id} not found")

# delete
@app.delete(
    path="/logentries/{log_entry_id}",
    response_model=LogEntryResponse,
    status_code=200,
    tags=["log_entry", "delete"],
    summary="delete entry by id",
    description="delete an entry by id. requires authentication, returns LogEntryResponse object of deleted item",
    responses={
        401: {"description": "Unauthorised — invalid or missing credentials"},
        422: {"description": "Validation error — request body did not match the expected schema"},
    })
def delete_log_entry(log_entry_id: str, api_key: str = Depends(check_key_header)):
    for idx, log_entry in enumerate(log_entry_db):
        if log_entry["id"].lower() == log_entry_id.lower():
            deleted_entry = log_entry_db.pop(idx)
            write_data(log_entry_db)
            return deleted_entry
    raise HTTPException(status_code=404, detail=f"Log Entry: {log_entry_id} not found")