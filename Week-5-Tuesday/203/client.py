import httpx

BASE_URL = "http://127.0.0.1:8000"

def main():
    with httpx.Client(base_url = BASE_URL, timeout = 10.0) as client:
        health = client.get(url = "/health").raise_for_status().json()
        print(f"Health:\n{health}")
        print("-" * 50)

        summary = client.get(url = "/summary").raise_for_status().json()
        print(f"Summary:\n{summary}")
        print("-" * 50)

        # rows from health should be same as length of summary
        assert (health["rows"] == summary["orders"])

        by_category = client.get(url = "/by-category").raise_for_status().json()
        print(f"By Category:\n{by_category}")
        print("-" * 50)

        # parameterized request for orders
        page = client.get(url = "/orders", params = {"region": "East", "limit": 10}).raise_for_status().json()
        print(f"Orders from East:\n{page["results"]}")
        print("-" * 50)
        assert (len(page["results"]) <= page["limit"])

    print("Assertions passed.")

if __name__ == "__main__":
    main()