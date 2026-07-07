# Exercise 102 - Consume a Public API

## Overview
You will write a Python client with **`httpx`** that pulls data from a public
API (no authentication required), handles errors and timeouts robustly, and
prints and saves a **structured** result. This is the "consume" half of Day 1 -
the skill that begins nearly every ingestion pipeline you will ever write.

The emphasis is on **robustness**, not just getting one happy-path response.
A script that hangs forever on a slow server or crashes on a `404` is not
production-grade; yours will handle both.

## Learning Objectives
- Make GET (and one POST) requests with `httpx`.
- Send query parameters and read JSON responses.
- Apply `raise_for_status()` and always set a **timeout**.
- Handle both failure modes: `HTTPStatusError` and `RequestError`.
- Reuse a connection with an `httpx.Client`.
- Transform raw API JSON into a trimmed, structured shape and save it to disk.

## Exercise Mode
**Implementation / Code Lab.** You write and run a real script. Deliverables
are working functions and their observable output (console + a saved file).

## Prerequisites / Setup
- Python 3.10+.
- Internet access.
- Read note **105** and skim demo **102** first.

```bash
mkdir my-api-client && cd my-api-client
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install "httpx>=0.28"
```

**Choose a no-auth public API.** Any of these work (pick one as your primary):
- `https://api.github.com` - repos, users, issues (structured, reliable)
- `https://httpbin.org` - echoes requests (great for POST/params, but flaky)
- `https://api.publicapis.org/entries` - a directory of public APIs
- `https://api.open-meteo.com/v1/forecast?latitude=40.7&longitude=-74&hourly=temperature_2m` - weather, no key

If your chosen API is down, fall back to GitHub.

## Part 1 - A single robust GET
Write a function that fetches one resource and returns parsed JSON, with a
timeout and `raise_for_status()`.

Starter:
```python
import httpx

def fetch_json(url: str, params: dict | None = None) -> dict:
    resp = httpx.get(url, params=params, timeout=10.0)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    data = fetch_json("https://api.github.com/repos/encode/httpx")
    print(data["full_name"], data["stargazers_count"])
```

**Deliverable:** A function that returns parsed JSON from your API, with an
explicit `timeout` and `raise_for_status()`.

**Acceptance criteria:**
- Uses `params=` for any query parameters (no hand-built query strings).
- Sets a `timeout`.
- Calls `raise_for_status()`.

## Part 2 - Error handling for both failure modes
Wrap your fetch so it distinguishes a **bad HTTP status** (server reached, e.g.
`404`/`500`) from a **transport failure** (never reached / timed out), and
returns `None` on failure instead of crashing.

Starter:
```python
def safe_fetch(url: str, params: dict | None = None) -> dict | None:
    try:
        resp = httpx.get(url, params=params, timeout=10.0)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as exc:
        print(f"Bad status {exc.response.status_code} from {url}")
    except httpx.RequestError as exc:
        print(f"Could not reach {url}: {type(exc).__name__}")
    return None
```

Prove it works by calling it against:
- a valid URL (returns data),
- a URL that 404s (e.g. `https://api.github.com/repos/encode/does-not-exist-xyz`),
- an unreachable host (e.g. `https://this-host-does-not-exist.example`).

**Deliverable:** `safe_fetch` handles all three cases without crashing, and
you print a clear message for each.

**Acceptance criteria:**
- `HTTPStatusError` and `RequestError` are caught **separately**.
- Failures return `None`; the program keeps running.

## Part 3 - Query parameters and (optionally) a POST
Make at least one request that uses **query parameters** to shape the result
(pagination, filtering, or search). If your API supports POST (e.g. httpbin),
also do one POST with a JSON body and confirm what the server received.

Starter:
```python
# GET with query params (GitHub issues, 5 per page)
issues = safe_fetch(
    "https://api.github.com/repos/encode/httpx/issues",
    params={"per_page": 5, "state": "open"},
)

# (Optional) POST with a JSON body
resp = httpx.post("https://httpbin.org/post",
                  json={"name": "Widget", "price": 9.99}, timeout=10.0)
print(resp.json()["json"])   # httpbin echoes what it received
```

**Deliverable:** At least one request driven by query parameters; the number
or content of results visibly changes when you change the params.

**Acceptance criteria:**
- Query params passed via `params=`.
- (If applicable) POST sends `json=` and you read the response.

## Part 4 - Reuse a Client and structure the output
Use an `httpx.Client` context manager (shared `base_url` / `headers` /
`timeout`) to make **two or more** related calls. Then transform the raw JSON
into a **trimmed structure** (keep only the fields you care about) and:
1. print the structured result, and
2. save it to a JSON file on disk.

Starter:
```python
import json
import httpx

def collect_repo(owner: str, name: str) -> dict | None:
    with httpx.Client(
        base_url="https://api.github.com",
        headers={"Accept": "application/vnd.github+json"},
        timeout=10.0,
    ) as client:
        try:
            repo = client.get(f"/repos/{owner}/{name}")
            repo.raise_for_status()
        except httpx.HTTPError as exc:
            print(f"Failed: {exc}")
            return None
        d = repo.json()
        return {
            "full_name": d["full_name"],
            "stars": d["stargazers_count"],
            "language": d["language"],
            "open_issues": d["open_issues_count"],
        }

result = collect_repo("encode", "httpx")
if result:
    print(result)
    with open("output.json", "w") as f:
        json.dump(result, f, indent=2)
```

**Deliverable:** A structured Python dict/list built from the API response,
printed to the console **and** saved to a `.json` file.

**Acceptance criteria:**
- Uses an `httpx.Client` context manager for at least two calls (or two fetched
  resources).
- Output is a trimmed structure (not the raw full response).
- A JSON file is written to disk.

## Definition of Done
- [ ] Script runs top to bottom with `python <script>.py`.
- [ ] Every request sets a `timeout` and uses `raise_for_status()` (or handles status).
- [ ] `HTTPStatusError` and `RequestError` are caught separately; failures don't crash the script.
- [ ] At least one request uses query parameters via `params=`.
- [ ] An `httpx.Client` context manager is used for related calls.
- [ ] The final result is a trimmed structure, printed and saved to a JSON file.

## Submission
Submit your project folder (excluding `.venv/`) containing:
- your client script,
- `requirements.txt` (`pip freeze > requirements.txt`),
- the generated `output.json`,
- a short `README.md` naming the API you consumed, how to run the script, and
  what the output represents.

## Time Estimate
**1.5-2.0 hours.** Parts 1-2 core (~50 min); Parts 3-4 (~50 min).

## Resources
- notes/105-consuming-apis-with-python-http-client.md
- demos/102-http-client-consume/ (reference implementation)
- [httpx QuickStart](https://www.python-httpx.org/quickstart/)
- [httpx Exceptions](https://www.python-httpx.org/exceptions/)
- [GitHub REST API](https://docs.github.com/en/rest)
- [httpbin](https://httpbin.org/)

## Rubric

| Criterion | Points | What earns full marks |
|-----------|-------:|------------------------|
| Script runs | 10 | Executes top to bottom without unhandled crashes |
| Basic GET + JSON parsing | 15 | Fetches and parses JSON from the chosen API |
| Timeouts | 10 | Every request sets an explicit `timeout` |
| `raise_for_status` | 10 | Used (or status explicitly checked) on responses |
| Error handling (two modes) | 20 | `HTTPStatusError` and `RequestError` caught separately; no crash on failure |
| Query parameters | 10 | At least one request shaped via `params=` |
| Client reuse | 10 | `httpx.Client` context manager used for related calls |
| Structured output + save | 10 | Trimmed structure printed and written to a JSON file |
| Code quality & README | 5 | Readable functions; clear README naming the API and run steps |
| **Total** | **100** | |
