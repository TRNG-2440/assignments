import httpx
import json

GITHUB_URL = "https://api.github.com" # part 1 - robust GET base url
BAD_URL = "https://bananagram.com" # part 2 - error handling url (doesn't exist)
BIN_URL = "https://httpbin.org" # part 3 - POST request

def fetch_json(base: str, url: str, params: dict | None = None) -> dict | None:
    with httpx.Client(base_url = base, timeout = 10.0) as client:
        try:
            resp = client.get(url, params = params)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            print(f"Bad status {e.response.status_code} from {base + url}")
        except httpx.RequestError as e:
            print(f"Could not reach {base + url}: {type(e).__name__}")
        return None

def collect_repo(owner: str, name: str) -> dict | None:
    with httpx.Client(
        base_url = "https://api.github.com",
        headers = {
            "Accept": "application/vnd.github+json"
        },
        timeout = 10.0
    ) as client:
        try:
            repo = client.get(f"/repos/{owner}/{name}")
            repo.raise_for_status()
        except httpx.HTTPError as e:
            print(f"Failed: {e}")
            return None
        d = repo.json()
        return {
            "full_name": d["full_name"],
            "stars": d["stargazers_count"],
            "language": d["language"],
            "open_issues": d["open_issues_count"],
        }


if __name__ == "__main__":
    # part 1

    data = fetch_json(base = GITHUB_URL, url = "/repos/encode/httpx")
    print(data)

    # part 2

    # 404 result
    data = fetch_json(base = GITHUB_URL, url = "/encode/does-not-exist-bananas")
    print(data)

    # unreachable host
    data = fetch_json(base = BAD_URL, url = "")
    print(data)

    # part 3
    
    # parameterized request
    params = {"per_page": 5, "state": "open"}
    print(fetch_json(base = GITHUB_URL, url = "/repos/encode/httpx/issues", params = params))
    print("-" * 50)

    # POST request
    payload = {
        "name": "Widget",
        "price": 10.99
    }
    post_resp = httpx.post(BIN_URL + "/post", json = payload, timeout = 10.0)
    print(post_resp.json()["json"]) # httpbin echoes payload

    # part 4
    result = collect_repo("William-Mahnke", "weather_project")
    if result:
        print(result)
        with open("output.json", "w") as f:
            json.dump(result, f, indent = 2)