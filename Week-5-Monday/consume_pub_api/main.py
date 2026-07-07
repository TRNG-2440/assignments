import httpx
import json

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

def safe_fetch(url: str, params: dict | None = None) -> dict | None:
    try:
        resp = httpx.get(url, params=params, timeout=10.0)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        print(e)
    except httpx.RequestError as e:
        print(e)
    return None

def fetch_json(url: str, params: dict | None = None) -> dict:
    resp = httpx.get(url, params=params, timeout=10.0)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    url = "https://api.github.com/repos/encode/httpx"
    
    # data = safe_fetch(url)
    issues = safe_fetch(url, params={"per_page": 5, "state": "open"})
    resp = httpx.post("https://httpbin.org/post", json={"name": "Widget", "price": 9.99}, timeout=10.0)
    print(resp.status_code)
    print(resp.headers)
    print(resp.text)
    print("-----------")

    result = collect_repo("encode", "httpx")
    if result:
        print(result)
        with open("output.json", "w") as f:
            json.dump(result, f, indent=2)

