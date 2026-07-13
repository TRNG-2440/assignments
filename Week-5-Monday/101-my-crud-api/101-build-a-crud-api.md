# Exercise 101 - Build a CRUD API

## Overview

You will build your own FastAPI service that exposes full **CRUD** (Create,
Read, Update, Delete) over a resource of your choice, backed by an in-memory
store. This is the "serve" half of Day 1. By the end you will have a running
API with interactive docs, proper status codes, validation, and `404`
handling - the foundation every Data API is built on.

You are **not** copying demo 101 line for line. Pick a *different* resource so
you actually think through the models and routes yourself.

## Learning Objectives

- Stand up a FastAPI app run by Uvicorn.
- Model a resource with Pydantic v2, using separate request and response models.
- Implement list / get-one / create / replace / delete endpoints.
- Use path params, query params, and a JSON request body.
- Return correct status codes (`200`, `201`, `204`, `404`, `422`).
- Organize routes with an `APIRouter`.
- Verify your API through the auto-generated `/docs`.

## Exercise Mode

**Implementation / Code Lab.** You write and run real code. Deliverables are
working endpoints you can demonstrate in `/docs` or with `curl`.

## Prerequisites / Setup

- Python 3.10+ (for the `X | None` type-hint syntax).
- Read notes **101-104** and skim demo **101** before starting.

```bash
mkdir my-crud-api && cd my-crud-api
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install "fastapi>=0.135" "uvicorn>=0.42" "pydantic>=2.10"
```

Suggested layout (a single `main.py` is acceptable for Part 1-2; split into a
router for Part 5):

```text
my-crud-api/
+-- app/
|   +-- __init__.py
|   +-- main.py
|   +-- models.py
|   +-- routers/
|       +-- __init__.py
|       +-- <resource>.py
+-- requirements.txt
```

Run your app at any time with:

```bash
uvicorn app.main:app --reload      # if using the app/ package layout
# or, if everything is in one file main.py:
uvicorn main:app --reload
```

**Pick your resource now.** Examples: `books`, `movies`, `sensors`,
`datasets`, `customers`, `songs`. Whatever you choose, it needs at least
**four fields** including one number and one boolean.

## Part 1 - App skeleton and health check

Create the FastAPI app and a root/health endpoint.

Starter:

```python
from fastapi import FastAPI

app = FastAPI(title="My CRUD API", version="0.1.0")

@app.get("/")
def read_root():
    return {"status": "ok"}
```

**Deliverable:** `uvicorn` starts without error, `GET /` returns `200` with a
JSON body, and `http://127.0.0.1:8000/docs` loads.

**Acceptance criteria:**

- Server runs with `--reload`.
- `/docs` shows your root endpoint.

## Part 2 - Pydantic models

Define **two** models for your resource: a create/input model (no id) and an
output model (with a server-assigned id). Add at least one `Field` constraint.

Starter (adapt the fields to your resource):

```python
from pydantic import BaseModel, Field

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str
    year: int = Field(gt=0)
    available: bool = True

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    year: int
    available: bool
```

**Deliverable:** Both models defined, with at least one `Field(...)` constraint
(e.g. `gt`, `min_length`).

**Acceptance criteria:**

- Input model has **no** `id`.
- Output model **includes** `id`.

## Part 3 - Create and read

Implement:

- `POST /<resource>` -> creates an item, assigns an id, returns it with `201`.
- `GET /<resource>/{id}` -> returns one item, or `404` if missing.
- `GET /<resource>` -> returns the list.

Starter:

```python
from fastapi import HTTPException, status

_DB: dict[int, dict] = {}
_next_id = 1

@app.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate):
    global _next_id
    record = {"id": _next_id, **payload.model_dump()}
    _DB[_next_id] = record
    _next_id += 1
    return record

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int):
    item = _DB.get(book_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Book {book_id} not found")
    return item

# TODO: GET /books  -> list, with response_model=list[BookOut]
```

**Deliverable:** You can create an item and read it back by id; a missing id
returns `404`.

**Acceptance criteria:**

- `POST` returns `201` and the created object with an `id`.
- `GET /<resource>/{id}` returns the item; unknown id returns `404` with a
`{"detail": ...}` body.
- Return **dicts or models** - do not call `json.dumps()`.

## Part 4 - Update, delete, and a query filter

Implement:

- `PUT /<resource>/{id}` -> replaces an existing item, `404` if missing.
- `DELETE /<resource>/{id}` -> deletes, returns `204 No Content`, `404` if missing.
- Add a **query parameter** to `GET /<resource>` that filters the list (e.g.
`?available=true` or `?limit=10`).

Starter:

```python
@app.get("/books")
def list_books(available: bool | None = None, limit: int = 50):
    rows = list(_DB.values())
    if available is not None:
        rows = [r for r in rows if r["available"] == available]
    return rows[:limit]

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    if book_id not in _DB:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Book {book_id} not found")
    del _DB[book_id]
    return None
# TODO: implement PUT /books/{book_id}
```

**Deliverable:** All five CRUD operations work; the list endpoint supports at
least one filter/pagination query parameter.

**Acceptance criteria:**

- `PUT` replaces an item and returns it; missing id -> `404`.
- `DELETE` returns `204` with an empty body; missing id -> `404`.
- The query filter changes the returned list.

## Part 5 - Refactor to an APIRouter

Move all `<resource>` endpoints into `app/routers/<resource>.py` behind an
`APIRouter(prefix="/<resource>", tags=["<resource>"])`, and mount it from
`main.py` with `app.include_router(...)`. See demo 101's structure.

**Deliverable:** Endpoints live in a router module; `main.py` only creates the
app and includes the router. Everything still works and is grouped under one
tag in `/docs`.

**Acceptance criteria:**

- `main.py` contains `app.include_router(...)`.
- The route paths are unchanged from Part 4 (the prefix supplies the resource
path).
- `/docs` shows your endpoints grouped under the resource tag.

## Definition of Done

- [x] App runs with `uvicorn ... --reload` and `/docs` loads.
- [x] Two Pydantic models (input without id, output with id); at least one `Field` constraint.
- [x] All five CRUD endpoints implemented and working.
- [x] Correct status codes: `201` create, `204` delete, `404` not-found, `422` invalid body.
- [x] At least one query parameter filters/pages the list endpoint.
- [x] Endpoints organized behind an `APIRouter`.
- [x] Returns dicts/models (no `json.dumps()` on returns).

## Submission

Submit your project folder (excluding `.venv/`) containing:

- the `app/` package (or `main.py`),
- a `requirements.txt` (`pip freeze > requirements.txt`),
- a short `README.md` with your chosen resource, the run command, and 3-4
example `curl` calls that exercise create / read / update / delete.

Be ready to demo the flow live in `/docs`.

## Time Estimate

**2.0-2.5 hours.** Parts 1-4 are the core (~~90 min); Part 5 refactor (~~30 min).

## Resources

- notes/101-fastapi-and-http-fundamentals.md
- notes/102-fastapi-routing-and-parameters.md
- notes/103-pydantic-models-and-validation.md
- notes/104-fastapi-interactive-docs.md
- demos/101-crud-fastapi/ (reference implementation)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

## Rubric

| Criterion | Points | What earns full marks |

|-----------|-------:|------------------------|
| App runs & docs load | 10 | Starts under Uvicorn; `/docs` renders all endpoints |
| Pydantic models | 15 | Separate input/output models; input has no id; >=1 `Field` constraint |
| Create (POST) | 15 | Returns `201` + created object with server-assigned id |
| Read (GET one + list) | 15 | Get-one works; list works; unknown id -> `404` |
| Update (PUT) | 10 | Replaces item; missing id -> `404` |
| Delete (DELETE) | 10 | Returns `204`; missing id -> `404` |
| Query parameter | 10 | List endpoint supports a working filter/pagination param |
| APIRouter organization | 10 | Routes in a router module, mounted via `include_router` |
| Correctness & style | 5 | Returns dicts/models (no `json.dumps`); clean, readable code |
| **Total** | **100** | |
