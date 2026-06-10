# Variable & Type Explorer

## Objective
Practice type conversion and exception handling with Python's core data types.

## Setup
Create a new file called `type_explorer.py`.

## Instructions
1. Prompt the user for a single input value
2. The input will always be a `str` — print it and its type
3. Attempt to convert the input to each of the following types:
   - `int`
   - `float`
   - `bool`
4. For each conversion:
   - If it succeeds, print the converted value and its type
   - If it fails, catch the exception and print a message indicating the input can't be converted to that type

## Things to Try
Run the script multiple times with different inputs and observe the results:
- `42`
- `3.14`
- `hello`
- `0`
- (empty string — just press Enter)

## Note
`bool()` will never raise an exception — any string converts. Pay attention to what values produce `True` vs `False`. Is the result what you expected?