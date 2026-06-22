from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
import creds
import storage
import uuid

app = FastAPI()


security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = creds.username
    correct_password = creds.password
    
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

class create(BaseModel):
    mood_score: int = Field(..., ge=1, le=100, description="The mood score felt from 1 to 100")
    notes: str = Field(..., description="Notes correlating with the mood")

class response(BaseModel):
    id: str
    mood_score: int
    notes: str
    created_at: str


@app.post("/moods", response_model=response)
def create_mood(entry: create, username: str = Depends(verify_credentials)):
    current_entries = storage.read_data()
    
    new_entry = {
        "id": str(uuid.uuid4()),
        "mood_score": entry.mood_score,
        "notes": entry.notes,
        "created_at": datetime.now().isoformat()
    }
    
    current_entries.append(new_entry)
    
    storage.write_data(current_entries)
    
    return new_entry


@app.get("/moods", response_model=list[response])
def get_all_moods(username: str = Depends(verify_credentials)):
    return storage.read_data()


@app.get(
    "/moods/{mood_id}", 
    response_model=response,
    status_code=status.HTTP_200_OK,
    summary="Get a single entry by its ID"
)

def get_single_mood(mood_id: str, username: str = Depends(verify_credentials)):
    current_entries = storage.read_data()
    for entry in current_entries:
        if entry["id"] == mood_id:
            return entry
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Mood entry with the ID {mood_id} not found"
    )


@app.put(
    "/moods/{mood_id}", 
    response_model=response,
    status_code=status.HTTP_200_OK,
    summary="Update an existing mood entry",
    description="Modifies the mood score or notes entry found by its ID."
)
def update_mood(mood_id: str, updated_entry: create, username: str = Depends(verify_credentials)):
    current_entries = storage.read_data()
    
    for entry in current_entries:
        if entry["id"] == mood_id:
            entry["mood_score"] = updated_entry.mood_score
            entry["notes"] = updated_entry.notes
            
            storage.write_data(current_entries)
            return entry
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Mood entry with the ID {mood_id} not found"
    )


@app.delete(
    "/moods/{mood_id}", 
    status_code=status.HTTP_200_OK,
    summary="Delete a mood entry",
    description="Permanently removes a mood record from the JSON file by its unique ID."
)


def delete_mood(mood_id: str, username: str = Depends(verify_credentials)):
    current_entries = storage.read_data()
    
    initial_length = len(current_entries)
    updated_entries = [entry for entry in current_entries if entry["id"] != mood_id]
    
    if len(updated_entries) == initial_length:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mood entry with ID {mood_id} not found"
        )
        
    storage.write_data(updated_entries)
    return {"message": f"Mood entry {mood_id} successfully deleted"}