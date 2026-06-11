# Graceful Failure

## Objective
Practice identifying and handling exceptions across multiple functions.

## Setup
Create a new file called `graceful_failure.py` and paste in the following script:

```python
def parse_record(record):
    name = record["name"]
    score = int(record["score"])
    history = record["history"]
    return {"name": name, "score": score, "history": history}


def calculate_average(parsed):
    average = sum(parsed["history"]) / len(parsed["history"])
    return average


records = [
    {"name": "Alice", "score": "85", "history": [90, 80, 70]},
    {"name": "Bob", "score": "fish", "history": [60, 75]},
    {"name": "Charlie", "score": "92", "history": []},
    {"name": "Dave", "score": "78", "history": [88, 91, 74]},
]

for record in records:
    parsed = parse_record(record)
    average = calculate_average(parsed)
    print(f"{parsed['name']} scored {parsed['score']} with a historical average of {average:.2f}")
```

## Instructions
1. Run the script — it will crash before finishing
2. Identify the two different exceptions that occur across the records
3. Add exception handling so the script makes it through all 4 records
4. For records that fail, print a message that says what went wrong
5. Records that succeed should still print their results normally

## Expected Behavior
- Alice: prints successfully
- Bob: fails in `parse_record` (why?)
- Charlie: fails in `calculate_average` (why?)
- Dave: prints successfully