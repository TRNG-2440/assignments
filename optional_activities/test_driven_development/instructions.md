# Unit Converter — Test Driven Development Activity

## Objective

In this activity, you will practice **Test Driven Development (TDD)** by implementing a unit conversion module from scratch — guided entirely by a pre-written test suite. You will practice:

- Reading and interpreting existing tests to understand expected behaviour
- Implementing functions iteratively, using failing tests as your feedback loop
- Handling edge cases discovered through tests rather than upfront design
- Raising appropriate exceptions for invalid inputs
- Working with floating point arithmetic and numeric tolerances

---

## What is TDD?

Test Driven Development is a workflow where tests are written before implementation code. As a developer, your job is to write the minimum code needed to make each failing test pass — then move on to the next. The tests are the specification.

The typical TDD cycle is:

1. **Red** — Run the tests. They fail because nothing is implemented yet.
2. **Green** — Write just enough code to make the failing test pass.
3. **Refactor** — Clean up your implementation without breaking passing tests.
4. **Repeat** — Move to the next failing test.

---

## Setup

You are provided with one file: `test_unit_converter.py`. Do **not** modify this file.

Your task is to create a new file called `unit_converter.py` in the same directory and implement the functions required to make the test suite pass.

Run the test suite at any time with:

```bash
python -m unittest test_unit_converter.py -v
```

When you first run this, every test will fail with an `ImportError` — that is expected and is your starting point.

---

## Instructions

1. Open `test_unit_converter.py` and read through it carefully before writing any code. Pay attention to:
   - What functions are being imported at the top of the file
   - What inputs each test passes to those functions
   - What each test expects in return
   - What exceptions certain tests expect to be raised

2. Create `unit_converter.py` and begin implementing functions one at a time, working top-to-bottom through the test file. Pick the first failing test, write only enough code to make it pass, then move to the next. Avoid skipping ahead or implementing functions that no failing test is currently asking for.

3. Re-run the test suite frequently. Use the output to identify which tests are still failing and why.

4. The test file is the complete specification for what your module must implement — it defines every function name, every domain, and every unit. Do not look for a summary elsewhere; read the tests.

5. Pay close attention to the edge case tests at the bottom of the test file. These will tell you what kinds of invalid input your functions are expected to handle, and how.

6. All return values are numeric. Tests use a tolerance-based comparison helper (`approx`) rather than exact equality — you do not need to round your return values, but your results must be within ±0.01 of the expected value. Note that this is an absolute tolerance, not a rounding constraint; return the full-precision result of your calculation.

---

## Requirements Checklist

- [ ] `unit_converter.py` exists in the same directory as the test file
- [ ] All temperature conversion functions are implemented and their tests pass
- [ ] All weight conversion functions are implemented and their tests pass
- [ ] All distance conversion functions are implemented and their tests pass
- [ ] Functions raise `ValueError` for physically impossible inputs (e.g. temperatures below absolute zero, negative weights or distances)
- [ ] Functions raise `TypeError` for non-numeric inputs
- [ ] Floating point inputs are handled correctly — functions are not limited to integer arguments
- [ ] All tests pass when running `python -m unittest test_unit_converter.py -v`
- [ ] No modifications have been made to `test_unit_converter.py`

---

## Stretch Goals

- **Rounding Control** — Update each function to accept an optional `decimal_places` parameter that rounds the result to the specified precision before returning. This parameter must default to `None` (no rounding applied) so that all existing tests continue to pass unmodified — several tests assert against values with more than two decimal places of precision and will break if rounding is applied by default.

- **Bidirectional Dispatcher** — Write a single `convert(value, from_unit, to_unit)` function that accepts unit names as strings (e.g. `convert(100, "celsius", "fahrenheit")`) and dispatches to the correct conversion function. Consider what should happen when an unsupported unit name is passed.

- **Expand the Domains** — Add a new conversion domain not covered by the existing tests (e.g. volume, speed, or data storage). Write your own test cases for the new domain first, following the same structure as `test_unit_converter.py`, then implement the functions to make them pass.
