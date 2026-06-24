# Voting System Simulator — Logging Activity

## Objective

In this activity, you will configure and add logging to a pre-built voting system simulation. Rather than building the application itself, your focus is entirely on the logging layer — understanding what is already being logged, configuring how and where those log records are output, and adding meaningful log calls to the application's entry point. You will practice:

- Configuring Python's built-in `logging` module using `basicConfig` and manual handler setup
- Working with multiple log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`) and understanding when each is appropriate
- Attaching multiple handlers to route log output to both the console and a file simultaneously
- Defining and applying log formatters to produce structured, readable log output
- Reading existing logging calls across a multi-module application and understanding the `getLogger(__name__)` pattern
- Writing your own log calls in a new entry point script

---

## Application Overview

You are provided with four modules that together form a simple election vote processor. Do **not** modify any of these files.

| Module | Purpose |
|---|---|
| `vote_loader.py` | Reads raw vote entries line-by-line from a plain text file |
| `validator.py` | Checks each vote against the known candidate list; flags invalid and spoiled votes |
| `tallier.py` | Counts valid votes per candidate and logs a running total at DEBUG level |
| `results_reporter.py` | Determines and logs the election outcome, including narrow-margin and tie detection |

A sample input file `votes.txt` is also provided. It contains a mix of valid votes, case variations, invalid candidate names, and a blank line — inspect it before running your code.

---

## Setup

Install no additional packages — this activity uses only Python's built-in `logging` module.

Create a new file called `main.py` in the same directory as the four application modules. This is the only file you will write from scratch. All logging configuration must live here, and it must be applied **before** any of the application modules are called.

---

## Instructions

### Part 1 — Understand the existing logging calls

Before writing any code, read through all four application modules and note:
- Which logger name each module uses and why
- Which log levels are used and in what situations
- What information is included in each log message

This will inform how you configure the logging system — if you set the root logger to `WARNING`, for instance, most of the application's output will be silenced.

### Part 2 — Configure the logging system in `main.py`

In `main.py`, configure logging so that:

1. **All log records at `DEBUG` level and above** are written to a file called `election.log` in the same directory. Each line in this file should follow the format:
   ```
   YYYY-MM-DD HH:MM:SS - MODULE_NAME - LEVEL - message
   ```

2. **Log records at `INFO` level and above** are printed to the console. The console format should be more compact:
   ```
   LEVEL - message
   ```

3. Both handlers must be attached to the **root logger**. Do not use `basicConfig` for this — configure the root logger and its handlers manually using `logging.getLogger()`, `logging.FileHandler`, `logging.StreamHandler`, and `logging.Formatter`.

4. The root logger acts as a first-level gate — a log record must pass the root logger's level check before it is ever forwarded to any handler. If the root logger's level is set too high, records will be silently discarded before your `FileHandler` or `StreamHandler` ever sees them, regardless of how those handlers are configured. With this in mind, think carefully about what level the root logger itself should be set to.

### Part 3 — Write the entry point in `main.py`

After configuring logging, `main.py` should:

1. Define the list of valid candidates for this election: `["Alice", "Bob", "Carol", "Dave"]`

2. Call each application module in pipeline order:
   - Load votes from `votes.txt` using `vote_loader.load_votes()`
   - Validate the loaded votes using `validator.validate_votes()`
   - Tally the valid votes using `tallier.tally_votes()`
   - Report the results using `results_reporter.report_results()`

3. Create a logger for `main.py` itself using `logging.getLogger(__name__)` and add log calls that record:
   - An `INFO` message when the pipeline starts, including the path to the votes file
   - An `INFO` message when the pipeline completes successfully
   - An `ERROR` message (with the exception detail) if any stage raises an exception, followed by a clean exit

---

## Example Console Output

When your logging is correctly configured and `main.py` is run against `votes.txt`, the console should produce output similar to the following. Your exact vote counts and messages may differ — this is illustrative of format and level filtering, not exact content.

```
INFO - Voting pipeline starting. Loading from 'votes.txt'.
INFO - Attempting to load votes from 'votes.txt'.
INFO - Successfully loaded 24 vote(s) from 'votes.txt'.
INFO - Beginning validation of 24 vote(s) against 4 candidate(s): Alice, Bob, Carol, Dave.
INFO - Vote #1 accepted: 'Alice'.
INFO - Vote #2 accepted: 'Bob'.
...
WARNING - Vote #12 is invalid — 'Invalid Candidate' does not match any known candidate.
WARNING - Vote #14 is a spoiled ballot (empty entry) — excluded from tally.
...
INFO - Validation complete — 21 valid, 2 invalid, 1 spoiled.
INFO - Starting vote tally for 21 valid vote(s).
INFO -   Alice                7 vote(s)
INFO -   Bob                  6 vote(s)
INFO -   Carol                5 vote(s)
INFO -   Dave                 3 vote(s)
INFO - Tally complete. Total valid votes counted: 21.
INFO - Determining election result from tally of 21 total vote(s).
INFO - RESULT — 'Alice' wins the election with 7 vote(s) (margin: 1 vote(s), 4.8% of total).
INFO - Pipeline completed successfully.
```

> **NOTE:** The example above is for illustrative purposes — your exact vote counts and candidate results will depend on `votes.txt` and how your pipeline processes the input.

Notice that `DEBUG`-level messages (the per-vote running totals from `tallier.py`) do **not** appear in the console output — they are filtered out by the console handler's level, but will be present in `election.log`.

---

## Requirements Checklist

- [ ] `main.py` exists in the same directory as the four application modules
- [ ] A `FileHandler` writing to `election.log` is configured with `DEBUG` level and the correct timestamp format
- [ ] A `StreamHandler` writing to the console is configured with `INFO` level and the compact format
- [ ] Both handlers are attached to the root logger — not to individual module loggers
- [ ] The root logger's level is set correctly so records are not silently discarded before reaching handlers
- [ ] `main.py` defines the candidate list and calls all four pipeline stages in order
- [ ] `main.py` uses `getLogger(__name__)` for its own logger
- [ ] `main.py` logs a start message, a completion message, and any pipeline exceptions at `ERROR` level
- [ ] `election.log` is produced when `main.py` is run and contains `DEBUG`-level records not visible on the console
- [ ] Console output shows only `INFO` and above — `DEBUG` messages are absent
- [ ] Application module files (`vote_loader.py`, `validator.py`, `tallier.py`, `results_reporter.py`) have not been modified

---

## Stretch Goals

- **Log Rotation** — Replace the `FileHandler` with a `RotatingFileHandler` from `logging.handlers`. Configure it to rotate `election.log` when it reaches 10KB, keeping a maximum of 3 backup files. Run the pipeline repeatedly to observe the rotation in action.

- **Separate Error Log** — Add a second `FileHandler` that writes only `WARNING` level and above to a separate file called `election_warnings.log`. This mirrors a common production pattern where errors are isolated for alerting and monitoring.

- **JSON Formatted Logging** — Replace the file handler's plain-text formatter with one that outputs each log record as a single-line JSON object (keys: `timestamp`, `module`, `level`, `message`). You will need to subclass `logging.Formatter` and override its `format` method to achieve this.

- **Config File Driven Setup** — Move all logging configuration out of `main.py` and into a `logging_config.json` file. Use `logging.config.dictConfig()` to load it at startup. This reflects how logging is typically managed in production Python applications.
