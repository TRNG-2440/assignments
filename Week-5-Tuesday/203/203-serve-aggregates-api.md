# Exercise 203 — Serve Aggregates API

## Overview

You'll build a small FastAPI service that loads a dataset into pandas at startup
and exposes endpoints returning **pandas-computed aggregates as JSON** — pulling
together Day 1 (FastAPI + `httpx`) and today (pandas). You start from the pattern
in [`demos/203-dataframe-api/`](../demos/203-dataframe-api/) and extend it with
your own aggregation, a filtered/paginated endpoint, and a client that consumes it.

## Learning Objectives

By the end you can:

- Load a CSV into a cached DataFrame at app startup (lifespan)
- Compute `groupby`/`agg` results and return them as JSON (`to_dict(orient="records")`)
- Add query parameters, a filter, and `limit`/`offset` pagination
- Handle the JSON gotchas: `reset_index()` after groupby, `NaN` → `null`
- Consume your own API with an `httpx` client

## Exercise Mode

**Build on the demo.** Copy the demo's routes/services/models structure as your
starting skeleton, then implement the required new endpoints. You may keep it a
single file if you prefer, but the layered structure is recommended and graded
lightly.

## Prerequisites / Setup

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install fastapi uvicorn pandas httpx
```

**Dataset:** reuse the `data/sales.csv` from
[`demos/203-dataframe-api/data/sales.csv`](../demos/203-dataframe-api/data/sales.csv)
(copy it into your project), **or** generate your own transactions CSV (the one
from exercise 201 works well — it has stores, categories, quantities, prices).
Whatever you use, it must have at least: an id, a category-like column, a
region/store-like column, and a numeric measure you can aggregate.

Run your app with:

```bash
uvicorn app.main:app --reload      # or: uvicorn main:app --reload if single-file
```

---

## Part 1 — Startup load + health

Load the CSV **once** at startup (FastAPI `lifespan`) into a cached DataFrame and
add any derived measure you need (e.g. `revenue = quantity * unit_price`).
Expose `GET /health` returning `{"status": "ok", "rows": <row count>}`.

**Deliverable:** `curl /health` returns the correct row count.
**Acceptance:** the CSV is read a single time at startup, **not** per request
(the read call is in the lifespan/startup path, not inside the route).

## Part 2 — Summary endpoint

`GET /summary` returns dataset-wide stats as JSON, at minimum:

- total number of records,
- total of your numeric measure,
- average of your numeric measure,
- number of distinct categories (`nunique`).

**Deliverable:** `curl /summary` returns a JSON object with those keys.
**Acceptance:** values are plain JSON numbers (cast numpy types with
`int(...)`/`float(...)` or `round(...)`), not numpy objects.

## Part 3 — Group aggregate endpoint

`GET /by-category` (or `/by-<your-group>`) returns one JSON object **per group**
with a count, a sum, and an average of your measure. Sort descending by the sum.

**Deliverable:** `curl /by-category` returns a JSON **array** of group objects.
**Acceptance:** the group key appears as a field in each object (you called
`reset_index()` after the groupby), and results are sorted by the summed measure.

## Part 4 — Filtered + paginated endpoint

`GET /records` returns raw rows with:

- an optional filter query param (e.g. `?region=East` or `?category=Widgets`),
- `limit` and `offset` query params for pagination (give sensible defaults and
  bounds via `Query(..., ge=..., le=...)`),
- a response envelope `{"total": N, "limit": L, "offset": O, "results": [...]}`
  where `total` is the count **before** paging.

Any `NaN` in the data must serialize as JSON `null`, not `NaN`.

**Deliverable:** show three calls:
`/records`, `/records?<filter>=<value>`, and `/records?limit=5&offset=5`.
**Acceptance:** the filter narrows results; paging returns the right slice;
`total` reflects the filtered count; an out-of-range `limit` returns HTTP 422.

## Part 5 — Consume it with httpx

Write `client.py` that (with the server running) calls at least three of your
endpoints with `httpx`, prints the JSON, and asserts one sanity check
(e.g. `assert summary["records"] == health["rows"]`, or that the paginated
`results` length ≤ `limit`).

**Deliverable:** `python client.py` prints responses and the assertion passes.
**Acceptance:** uses `httpx` (not `requests`); at least one meaningful assertion
that would fail if an endpoint were wrong.

---

## Definition of Done

- App starts with `uvicorn ...` and all endpoints respond.
- `/health`, `/summary`, `/by-category`, `/records` all work as specified.
- CSV is loaded once at startup; groupby uses `reset_index()`; `NaN` → `null`.
- `client.py` runs green against the live server.
- `/docs` renders (bonus: your response models are typed).

## Submission

Submit your app code (single file or `app/` package), `client.py`, and your
`requirements.txt`. In the PR description paste: the `client.py` output and one
screenshot **or** curl transcript of `/by-category`.

## Time Estimate

**75–120 minutes.**

## Resources

- [`notes/204-serving-data-through-fastapi.md`](../notes/204-serving-data-through-fastapi.md)
- [`demos/203-dataframe-api/`](../demos/203-dataframe-api/) — start from this pattern
- [`notes/201-pandas-refresher.md`](../notes/201-pandas-refresher.md) — groupby/agg
- FastAPI query params: <https://fastapi.tiangolo.com/tutorial/query-params/>
- httpx quickstart: <https://www.python-httpx.org/quickstart/>

## Rubric (100 points)

| Criterion | Points |

|-----------|--------|
| Part 1 — startup load (once) + /health | 15 |
| Part 2 — /summary with correct JSON-native stats | 15 |
| Part 3 — group aggregate, reset_index, sorted | 20 |
| Part 4 — filter + pagination + envelope + NaN→null | 25 |
| Part 5 — httpx client with a real assertion | 15 |
| Layered/clean structure, /docs renders, runs green | 10 |
| **Total** | **100** |
