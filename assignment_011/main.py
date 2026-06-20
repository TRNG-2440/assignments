from fastapi import FastAPI, HTTPException
from models import LogEntryCreate, LogEntryResponse, LogEntryUpdate
from uuid import uuid4
from datetime import datetime
from storage import read_data, write_data
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
@app.get("/logentries/{log_entry_id}", response_model=LogEntryResponse, tags=["logentry"])
def get_log_entry(log_entry_id: str):
    for log_entry in log_entry_db:
        if log_entry["id"].strip().lower() == log_entry_id.strip().lower():
            return log_entry
    raise HTTPException(status_code=404, detail=f"log entry with ID {log_entry_id} not found")

# create
@app.post("/logentries", response_model=LogEntryResponse, tags=["logentry"])
def create_log_entry(log_entry: LogEntryCreate):
    new_log_entry = {
        "id": str(uuid4()),
        "created_at": str(datetime.now()),
        "activity": log_entry.activity,
        "description": log_entry.description,
        "location" : log_entry.location
    }
    log_entry_db.append(new_log_entry)
    write_data(log_entry_db)
    return new_log_entry

# update
@app.patch("/logentries/{log_entry_id}", response_model=LogEntryResponse, tags=["logentry"])
def update_log_entry(log_entry_id: str, log_entry_update: LogEntryUpdate):
    for idx, log_entry in enumerate(log_entry_db):
        if log_entry["id"] == log_entry_id:
            updated_fields = log_entry_update.model_dump(exclude_none=True)
            log_entry_db[idx].update(updated_fields)
            write_data(log_entry_db)
            return log_entry
    raise HTTPException(status_code=404, detail=f"Log Entry: {log_entry_id} not found")

@app.delete("/logentries/{log_entry_id}", response_model=LogEntryResponse, tags=["logentry"])
def delete_log_entry(log_entry_id: str):
    for idx, log_entry in enumerate(log_entry_db):
        if log_entry["id"] == log_entry_id:
            deleted_entry = log_entry_db.pop(idx)
            write_data(log_entry_db)
            return deleted_entry
    raise HTTPException(status_code=404, detail=f"Log Entry: {log_entry_id} not found")