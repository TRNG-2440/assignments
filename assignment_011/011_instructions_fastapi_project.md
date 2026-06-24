# FastAPI Group Project

## Overview

In this project, your team of up to 3 will design and build a fully functional REST API using **FastAPI**. Your API will persist data using JSON files, require authentication on protected endpoints, and be fully explorable through FastAPI's built-in **Swagger UI** — no frontend required.

This project is intentionally open-ended. Within the guidelines below, your team makes the design decisions: what your data model looks like, how your endpoints are structured, and what your API is capable of. The goal is to produce something you could hand to another developer and have them use it entirely through Swagger.

---

## Step 1 — Team Setup

Before any technical work begins, complete the following:

1. **Elect a Team Captain.** If you are working as a team, elect a captain before beginning. The Team Captain is responsible for coordinating the team's decisions, resolving disagreements on API design, and helping coordinate the presentation of your API at the end of the project (see Deliverables).

2. **Select a project topic.** Select an option from the list below, or speak to your trainer about another idea to ensure the project is sound, before moving forward. Each team must choose a different topic — selections are first-come, first-served. Confirm your choice with the facilitator before beginning.

### Available Project Topics

| # | Topic | Description |
|---|---|---|
| 1 | **Movie Watchlist** | Track films with watch status, ratings, and genre tags |
| 2 | **Mood Journal** | Log daily mood scores with notes and track emotional trends over time |
| 3 | **Travel Log** | Record trips with destinations, dates, and highlights |
| 4 | **Meal Planner** | Plan weekly meals, link to a recipe store, and generate shopping list summaries |
| 5 | **Workout Log** | Track exercise sessions, sets, reps, and weights over time |
| 6 | **Reading List** | Manage a personal book collection with ratings and reading status |
| 7 | **Personal Budget Tracker** | Log income and expenses by category and analyse spending patterns |
| 8 | **Recipe & Nutrition Log** | Store recipes with nutritional data and log daily meals against them |
| 9 | **Pet Health Tracker** | Log vet visits, medications, weight, and health events for one or more pets |
| 10 | **Goal Tracker** | Log personal goals with deadlines, milestones, and completion status |
| 11 | **Wellness Tracker** | Log sleep hours, water intake, and exercise minutes daily |
| 12 | **Garden Journal** | Log plantings, harvests, soil conditions, and seasonal observations across garden beds |

---

## Step 2 — Project Setup

### Installation

Install FastAPI and a compatible server:

```bash
pip install fastapi uvicorn
```

### Running your API

```bash
uvicorn main:app --reload
```

### Swagger UI

Once running, your full API is explorable at:

```
http://127.0.0.1:8000/docs
```

Every endpoint your team defines will appear here automatically, including request schemas, response models, and the ability to make live test requests. Your Swagger UI is the primary interface for this project — make sure every endpoint is well-described.

### Project Structure

There is no single required file structure, but the following is a reasonable starting point for a project of this scope:

```
project/
├── main.py              # FastAPI app entry point, router registration
├── auth.py              # Authentication logic
├── models.py            # Pydantic request/response models
├── storage.py           # JSON file read/write helpers
├── routers.py           # Endpoint definitions
└── data/
    └── [your_topic].json  # Persistent data store
```

Your team may organise this differently — what matters is that the structure is logical and that responsibilities are clearly separated.

---

## Step 3 — Authentication

Every team must implement authentication on all non-public endpoints. Your team chooses **one** of the two following strategies:

### Option A — HTTP Basic Auth

FastAPI supports HTTP Basic Auth via the `HTTPBasic` security scheme. Credentials are extracted from the `Authorization` header and validated against expected values. A verification function can be defined and injected into endpoints as a dependency using `Depends`.

Key imports to get started:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
```

- Instantiate `HTTPBasic()` to create a security scheme
- Define a function that accepts `HTTPBasicCredentials` via `Depends` and raises an `HTTPException` with status `401` if the credentials do not match
- Inject your verification function into any endpoint that should be protected

---

### Option B — API Key Auth

API key authentication checks for a key passed as a request header. FastAPI supports this via the `APIKeyHeader` scheme. Like Basic Auth, the verification logic is written as a dependency function and injected into protected endpoints using `Depends`.

Key imports to get started:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
```

- Instantiate `APIKeyHeader(name="...")` with the header name your API will expect
- Define a function that accepts the extracted key via `Depends` and raises an `HTTPException` with status `403` if it does not match your expected value
- Inject your verification function into any endpoint that should be protected

---

> **Note:** For the purposes of this project, hardcoded credentials or a single API key are acceptable. In a production system, credentials would never be stored in plain text in source code.

---

## Step 4 — Data Persistence

All data must be stored in and read from **JSON files**. Do not use a database.

Your `storage.py` module should provide two reusable helper functions used throughout the rest of your application:

```python
# read_data(filepath):
#   - check if the file exists at the given path
#   - if it does not exist, return an empty list
#   - if it does, open it and load the contents as JSON
#   - return the loaded data

# write_data(filepath, data):
#   - open the file at the given path in write mode
#   - serialise 'data' as JSON and write it to the file
```

Each record your API stores should have a unique ID. You may generate IDs however you choose — a simple approach is to use Python's built-in `uuid` module:

```python
import uuid
new_id = str(uuid.uuid4())
```

---

## Step 5 — API Requirements

Your API must meet all of the following requirements regardless of topic.

### Data Models
- Define all request and response schemas using **Pydantic models**
- Every record must have a unique `id` field, auto-generated on creation
- Every record must have a `created_at` timestamp, auto-generated on creation
- Use appropriate types — do not store numbers as strings or dates as plain integers

### Endpoints
Your API must implement the following endpoint categories. The exact paths, field names, and behaviour are up to your team — design them to fit your chosen topic.

| Category | Requirement |
|---|---|
| **Create** (REQUIRED) | At least one `POST` endpoint that adds a new record |
| **Read (all)** (REQUIRED) | At least one `GET` endpoint that returns all records |
| **Read (single)** (REQUIRED) | At least one `GET` endpoint that returns a single record by ID |
| **Update** (REQUIRED) | At least one `PUT` or `PATCH` endpoint that modifies an existing record |
| **Delete** (REQUIRED) | At least one `DELETE` endpoint that removes a record by ID |
| **Filter/Query** (OPTIONAL) | At least one `GET` endpoint that accepts query parameters to filter or search records |
| **Summary/Insight** (OPTIONAL) | At least one `GET` endpoint that returns a computed summary or analytical result derived from the stored data |

### Authentication
- All endpoints except any intentionally public ones (e.g. a health check) must be protected by the authentication strategy your team selected
- Unauthenticated requests must receive an appropriate HTTP error response (`401` or `403`)

### Swagger Documentation
- Every endpoint must have a clear **summary** and **description** visible in Swagger
- All request bodies and response models must be fully described via Pydantic so Swagger renders accurate schemas
- HTTP status codes for both success and error responses should be declared on each endpoint

---

## Step 6 — Swagger Documentation Quality

Since Swagger is the primary interface for this project, documentation is a first-class deliverable — not an afterthought.

FastAPI generates Swagger documentation automatically from your code, but the quality depends on what your team provides. Make use of the following:

```python
@router.post(
    "/entries",
    response_model=EntryResponse,
    status_code=201,
    summary="Create a new entry",
    description="Adds a new record to the store. Requires authentication. Returns the created record including its auto-generated ID and timestamp.",
    responses={
        401: {"description": "Unauthorised — invalid or missing credentials"},
        422: {"description": "Validation error — request body did not match the expected schema"},
    }
)
def create_entry(...):
    ...
```

A reviewer should be able to open your Swagger UI and fully understand and test your API without reading a single line of source code.

---

## Deliverables

### 1. Source Code
A well-structured, commented Python project containing all source files. Submit as a `.zip` or via a shared repository.

### 2. Presentation
The team will give a **5 minute walkthrough** of the API using Swagger UI. Every team member must present at least one point during the walkthrough. The presentation should demonstrate:
- At least one protected endpoint (showing both an unauthenticated failure and an authenticated success)
- The create, read, and summary endpoints
- Data persistence in action — create or retrieve records live during the walkthrough
- One design decision the team made and why

---

## Requirements Checklist

- [ ] A Team Captain has been elected
- [ ] A project topic has been selected and confirmed with the facilitator
- [ ] The API is built using FastAPI and runs with `uvicorn`
- [ ] All data is persisted to and read from JSON files
- [ ] Pydantic models are defined for all request bodies and responses
- [ ] Every record has an auto-generated `id` and `created_at` field
- [ ] Authentication is implemented using either HTTP Basic Auth or API Key
- [ ] All non-public endpoints are protected and return `401`/`403` for unauthenticated requests
- [ ] CRUD endpoint categories are implemented (create, read all, read one, update, delete)
- [ ] Every endpoint has a Swagger summary, description, and declared response codes
- [ ] The team has prepared a 5-minute Swagger walkthrough
- [ ] Every team member presents at least one point during the walkthrough

---

## Stretch Goals

These are optional extensions for teams who complete the core requirements early. Each one introduces a concept beyond the core scope of the project.

- **Custom Exceptions** — Rather than raising generic `HTTPException` instances inline throughout your endpoints, define a set of custom exception classes (e.g. `RecordNotFoundError`, `DuplicateEntryError`) and register exception handlers with FastAPI using `@app.exception_handler`. This separates error-handling logic from endpoint logic and mirrors how production FastAPI applications manage errors.

- **Additional Response Payload Types** — Add at least one endpoint that returns a non-JSON payload. For example, a `GET /export/csv` endpoint that returns all records as a downloadable CSV file using FastAPI's `FileResponse`, or a `GET /summary/chart` endpoint that generates a matplotlib chart and returns it as a PNG image. Remember that additional Response types can be imported from `fastapi.responses`.

- **Session-Based Auth with Cookies** — Replace or supplement your current authentication strategy with cookie-based sessions. Add a `POST /login` endpoint that validates credentials and sets a signed session cookie using FastAPI's `Response` object, and a `POST /logout` endpoint that clears it. Protected endpoints then read and validate the session cookie rather than checking a header on every request. You will need to import `Response` and `Request` from `fastapi`.
