# Lab 3: Functions & Lambdas

So far you've written code that runs top to bottom. In this lab you'll learn to package code into **functions** — named, reusable blocks you can run on demand — and then meet their compact cousins, **lambdas**. Along the way you'll see one of Python's most powerful ideas: functions are values, and you can pass them around just like numbers or strings.

This lab has two parts:

1. **Guided Coding** — function syntax, then lambda syntax, with complete working examples.
2. **Exercise** — you build a calculator that's driven by lambdas.

---

## Part 1: Guided Coding

### 1.1 Function Syntax

A **function** is a named block of code that you define once and run (or "call") as many times as you like. Functions let you avoid repeating yourself, give meaningful names to chunks of logic, and break big problems into small pieces.

#### Defining and calling

The `def` keyword starts a function definition:

```python
def greet():
    print("Hello there!")
```

Anatomy of that definition:

- `def` — tells Python "a function definition starts here"
- `greet` — the function's name (same naming rules as variables)
- `()` — the parentheses hold parameters; this function has none
- `:` and the indented block — the **body**, the code that runs when the function is called

Defining a function doesn't run it. Nothing happens until you **call** it by writing its name followed by parentheses:

```python
def greet():
    print("Hello there!")

greet()
greet()
greet()
```

Output:

```
Hello there!
Hello there!
Hello there!
```

One definition, three calls. That's the whole point — write it once, use it anywhere.

#### Parameters

Functions become far more useful when you can pass information **into** them. Variables listed inside the parentheses of the definition are called **parameters**; the actual values you supply when calling are called **arguments**.

```python
def greet(name):
    print("Hello,", name + "!")

greet("Alice")
greet("Bob")
```

Output:

```
Hello, Alice!
Hello, Bob!
```

When `greet("Alice")` runs, the parameter `name` is set to `"Alice"` for the duration of that call. Each call gets its own fresh values.

A function can take multiple parameters, separated by commas — and the arguments are matched up **in order**:

```python
def describe_pet(animal, name):
    print("I have a", animal, "named", name + ".")

describe_pet("dog", "Rex")
describe_pet("cat", "Whiskers")
```

Output:

```
I have a dog named Rex.
I have a cat named Whiskers.
```

#### Return values

So far our functions only print. More often, you want a function to **compute** something and hand the result back to the caller. That's what `return` does:

```python
def add(a, b):
    return a + b

result = add(3, 4)
print(result)           # 7
print(add(10, 20))      # 30
```

Output:

```
7
30
```

Key things about `return`:

- The returned value lands wherever the call was made — you can store it in a variable, print it, or use it in a bigger expression like `add(1, 2) * 10`.
- `return` immediately **ends** the function. Any code after it in the body never runs.
- A function with no `return` statement returns the special value `None` automatically.

Here's a function that uses flow control (from Lab 1) and an early return together:

```python
def absolute_value(n):
    if n < 0:
        return -n       # for negatives, return the flipped sign...
    return n            # ...otherwise return the number as-is

print(absolute_value(-5))   # 5
print(absolute_value(12))   # 12
```

Output:

```
5
12
```

When `n` is negative, the first `return` fires and the function is done. When it isn't, Python falls through to the second `return`.

**Print vs. return — a common beginner mix-up:** `print()` shows a value to a human on the screen; `return` hands a value back to the *code* that called the function. If you want to use a function's result in further calculations, you need `return`.

---

### 1.2 Lambda Syntax

A **lambda** is a small, anonymous function written as a single expression. "Anonymous" means it doesn't need a name; "single expression" means the body is one expression whose value is automatically returned — no `return` keyword, no multi-line body.

The syntax:

```python
lambda parameters: expression
```

Compare a regular function with its lambda equivalent:

```python
# Regular function
def add(a, b):
    return a + b

# Lambda doing the same job, assigned to a variable
add_lambda = lambda a, b: a + b

print(add(3, 4))           # 7
print(add_lambda(3, 4))    # 7
```

Output:

```
7
7
```

Read the lambda left to right: "a function taking `a` and `b` that evaluates `a + b`." Once it's assigned to `add_lambda`, you call it exactly like any other function.

This works because in Python, **functions are values**. A `def` statement creates a function object and binds it to a name; a lambda creates a function object inline, and you can do whatever you like with it — assign it, store it in a list, or (most importantly) pass it to another function.

> **Style note:** assigning a lambda to a variable, as above, is great for learning the syntax — but if you're naming it anyway, `def` is generally clearer. Lambdas earn their keep in the next section.

#### Lambdas inline — where they shine

The real power of lambdas is using them **without ever assigning them**, right at the spot where a function is needed. Several built-in functions accept a function as an argument, and lambdas fit there perfectly.

**Example 1: `sorted()` with a key.** The `sorted()` function accepts an optional `key` argument: a function it calls on each item to decide the sort order. Suppose we want to sort words by their **length** rather than alphabetically:

```python
words = ["banana", "kiwi", "apple", "fig"]

by_length = sorted(words, key=lambda word: len(word))
print(by_length)
```

Output:

```
['fig', 'kiwi', 'apple', 'banana']
```

The lambda `lambda word: len(word)` is created right there in the call, used by `sorted()` to measure each word, and never needs a name. It exists for exactly one job in exactly one place.

Here's the same idea sorting a list of (name, score) pairs by the score:

```python
scores = [("Alice", 88), ("Bob", 95), ("Carmen", 72)]

by_score = sorted(scores, key=lambda pair: pair[1])
print(by_score)
```

Output:

```
[('Carmen', 72), ('Alice', 88), ('Bob', 95)]
```

**Example 2: `map()`.** The `map()` function applies a function to every item of an iterable (Lab 2 vocabulary!) and produces the results. Wrapping it in `list()` collects them:

```python
numbers = [1, 2, 3, 4, 5]

squares = list(map(lambda n: n * n, numbers))
print(squares)
```

Output:

```
[1, 4, 9, 16, 25]
```

Again the lambda is born, does its job on each item, and is gone — **no assignment required**. That's the takeaway: a lambda doesn't need a name or a variable; it's a function expression you can drop in wherever a function is expected.

**When to use which:** if the logic fits in one short expression and is only needed in one spot, a lambda keeps the code compact. If it needs multiple statements, a docstring, or reuse, write a `def`.

---

## Part 2: Exercise — Calculator Function

Time to combine everything: you'll write a function that **takes another function as a parameter** — exactly the pattern `sorted(key=...)` and `map(...)` use, but now you're on the receiving side.

### Your task

Below is the **calling code** for a calculator. It calls a function named `calculator()`, passing in three arguments each time:

1. an **operation** — a lambda that does the actual math
2. two **operands** — the numbers to operate on

Your job has two parts:

1. **Write the `calculator()` function.** It takes the lambda and the two operands, applies the lambda to the operands, and returns the result.
2. **Write the four lambdas** — `add`, `subtract`, `multiply`, and `divide` — that the calling code passes in.

Copy this into a file; the calling code at the bottom must work **unmodified**:

```python
# TODO 1: define the calculator function here.
# It takes three parameters: an operation (a function) and two operands.
# It applies the operation to the operands and returns the result.


# TODO 2: define the four operation lambdas here.
# Each takes two parameters and evaluates to the result of the operation.
add = ...
subtract = ...
multiply = ...
divide = ...


# ---- Calling code: do not modify below this line ----

print(calculator(add, 6, 2))         # should print 8
print(calculator(subtract, 6, 2))    # should print 4
print(calculator(multiply, 6, 2))    # should print 12
print(calculator(divide, 6, 2))      # should print 3.0

# Lambdas don't need names — an inline lambda works too:
print(calculator(lambda a, b: a ** b, 6, 2))   # should print 36
```

### Expected output

```
8
4
12
3.0
36
```

### Hint 1: A function parameter is called like any function

Inside `calculator()`, the operation arrives as an ordinary parameter — let's say you name it `operation`. Since it holds a function, you call it the usual way: `operation(x, y)`. The skeleton is small:

```python
def calculator(operation, a, b):
    # call operation with a and b, and return what it gives back
    ...
```

Remember from the guided section: the result must be **returned**, not printed — the calling code does the printing.

### Hint 2: The lambdas are one-liners

Each lambda takes two parameters and evaluates to one expression. The `add` lambda looks structurally identical to the `add_lambda` example from section 1.2. The four operators you need are `+`, `-`, `*`, and `/`.

### Hint 3: Why does divide print `3.0` and not `3`?

Not a bug! Python's `/` operator always produces a float, even when the division is exact. If your output shows `3.0`, you've done it right.

### Check your work

- All five lines of output match the expected output exactly, including `3.0`.
- The last test passes a lambda **inline**, with no name at all — if your `calculator()` is written correctly, it works without any changes, because `calculator()` doesn't care whether its operation has a name.
- You didn't modify the calling code — only the TODOs above it.

### Stretch goal (optional)

If you finish early: add a `power` lambda using the `**` operator, and try writing a `calculator()` call that uses your `power` lambda to compute 2 to the 10th. Then try passing a *named function* (defined with `def`) instead of a lambda — confirm that `calculator()` doesn't care which kind it receives.

Good luck!
