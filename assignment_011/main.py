from fastapi import FastAPI
from assignment_011.models import LogEntryCreate, LogEntryResponse, LogEntryUpdate
from uuid import uuid4

app = FastAPI(
    title="Gardening API", 
    description="a gardening log data", 
    version="0.1.0"
)

@app.get("/logentries", response_model=LogEntryResponse, tags=["logentry"])
def get_log_entry():
    pass

@app.post("/logentries", response_model=LogEntryResponse, tags=["logentry"])
def create_log_entry(log_entry: LogEntryCreate):
    new_log_entry = {
        "id": (uuid4),
        "type": log_entry.type
    }
    return new_log_entry

@app.patch("/logentries", response_model=LogEntryResponse, tags=["logentry"])
def update_log_entry(log_entry: LogEntryUpdate):
    pass