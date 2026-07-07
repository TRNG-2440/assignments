# My CRUD API

A FastAPI service with full CRUD over a **movies** resource, backed by an in-memory store.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API docs.

## Example curl calls

```bash
# Create
curl -X POST http://127.0.0.1:8000/movies \
  -H "Content-Type: application/json" \
  -d '{"title":"Inception","director":"Christopher Nolan","year":2010,"in_theaters":false}'

# Read one
curl http://127.0.0.1:8000/movies/1

# Update
curl -X PUT http://127.0.0.1:8000/movies/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Inception","director":"Christopher Nolan","year":2010,"in_theaters":true}'

# Delete
curl -X DELETE http://127.0.0.1:8000/movies/1 -i
```
