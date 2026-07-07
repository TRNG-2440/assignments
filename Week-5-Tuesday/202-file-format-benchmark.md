# Exercise 202 — File Format Benchmark

## Overview

You'll benchmark **CSV vs JSONL vs Parquet** on file size and read/write time
across **two different row counts**, then write up what you found. The goal is to
turn the claims in [`notes/203-file-formats-csv-json-parquet.md`](../notes/203-file-formats-csv-json-parquet.md)
("Parquet is smaller and faster") into numbers you produced yourself — and to see
how the gap *changes with scale*.

## Learning Objectives

By the end you can:

- Write the same DataFrame to CSV, JSONL, and Parquet from pandas
- Measure file size and write/read time correctly
- Reason about *why* the formats differ (columnar + compression + type handling)
- Show that Parquet preserves types on a round-trip while CSV does not

## Exercise Mode

**Build + analyze.** You write a benchmark script and a short findings writeup.
[`demos/202-format-size-comparison/`](../demos/202-format-size-comparison/) is a
starting reference — but this exercise adds a **second row count** and a
**type-preservation check** that the demo doesn't have, so you must extend it.

## Prerequisites / Setup

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install pandas pyarrow numpy
```

Generate a mixed-type DataFrame (ints, floats, strings, bools, **and a datetime**
— the datetime matters for Part 3):

```python
import numpy as np, pandas as pd

def make_df(n):
    rng = np.random.default_rng(0)
    return pd.DataFrame({
        "id": np.arange(n),
        "name": [f"user_{i}" for i in range(n)],
        "dept": rng.choice(["A", "B", "C", "D"], n),
        "score": rng.uniform(0, 100, n).round(3),
        "active": rng.choice([True, False], n),
        "ts": pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 1000, n), unit="h"),
    })
```

---

## Part 1 — Benchmark harness

Write `benchmark.py` that, for a given row count, writes the DataFrame to CSV,
JSONL, and Parquet (Snappy), and records for each:

- **file size** (MB), and
- **write time** and **read time** in seconds (use `time.perf_counter()`).

Create the output directory if it doesn't exist (`os.makedirs(..., exist_ok=True)`).

**Deliverable:** a function/loop that returns or prints size + write + read for
all three formats at one row count.
**Acceptance:** all three files are actually written to disk and measured; times
use `perf_counter`, not wall-clock `time.time()` around unrelated work.

## Part 2 — Two scales

Run the benchmark at **two row counts** — e.g. `50_000` and `500_000` — and print
a combined table. Include a **size-ratio-vs-CSV** column for each format.

**Deliverable:** a printed table like:

```
rows     format    size_mb   vs_csv   write_s   read_s
50000    CSV       ...        1.00x    ...       ...
50000    JSONL     ...        ...      ...       ...
50000    Parquet   ...        ...      ...       ...
500000   CSV       ...        1.00x    ...       ...
...
```

**Acceptance:** both row counts appear; ratios are relative to that row count's
CSV size; Parquet's `vs_csv` ratio is well below 1.0 at both scales.

## Part 3 — Type preservation check

Read the **CSV** back and the **Parquet** back, and print `.dtypes` for each.
Show that:

- Parquet returns `ts` as `datetime64` and `active` as `bool`,
- plain `read_csv` returns `ts` as `object` (text) and `active` differently
  (unless you pass `parse_dates=`).

**Deliverable:** the two `.dtypes` printouts, side by side or labeled.
**Acceptance:** the difference is visible — Parquet preserved types, CSV lost them.

## Part 4 — Findings writeup

In a `FINDINGS.md` (150–300 words) answer:

1. Which format was smallest? By roughly what factor vs CSV, at each scale?
2. Did the **size gap widen** as rows grew from 50k to 500k? Why would columnar
   + compression scale better than row text?
3. Which format read fastest, and why (binary+typed vs text-parse)?
4. Given your numbers, when would you *still* choose CSV or JSONL over Parquet?
5. One sentence on the type-preservation result from Part 3 and why it matters
   for a pipeline.

**Deliverable:** `FINDINGS.md` grounded in *your* measured numbers (quote them).
**Acceptance:** each question answered; claims reference the actual table values,
not generic statements.

---

## Definition of Done

- `benchmark.py` runs with `python benchmark.py` and prints the two-scale table
  plus the Part 3 dtype comparison, with no errors.
- Output directory is created programmatically.
- `FINDINGS.md` is present and cites your real numbers.

## Submission

Submit `benchmark.py`, `FINDINGS.md`, and paste the console table into your PR
description. (No need to commit the generated data files.)

## Time Estimate

**45–75 minutes.**

## Resources

- [`notes/203-file-formats-csv-json-parquet.md`](../notes/203-file-formats-csv-json-parquet.md)
- [`demos/202-format-size-comparison/`](../demos/202-format-size-comparison/)
- pandas I/O reference: <https://pandas.pydata.org/docs/reference/io.html>

## Rubric (100 points)

| Criterion | Points |
|-----------|--------|
| Part 1 — correct harness, all 3 formats written + timed | 25 |
| Part 2 — two scales, combined table with vs-CSV ratios | 25 |
| Part 3 — type-preservation comparison shown clearly | 20 |
| Part 4 — findings cite real numbers, answer all 5 questions | 25 |
| Code runs clean; output dir created programmatically | 5 |
| **Total** | **100** |
