# Lab 1: Flow Control

Welcome to Lab 1! In this lab you'll learn how to control the *flow* of a Python program — that is, how to make your code make decisions and repeat actions. These are the most fundamental building blocks of programming, and you'll use them in every program you ever write.

This lab has two parts:

1. **Guided Coding** — read through each concept and run the example code yourself. Every example is complete and works as-is.
2. **Exercises** — you write the code. Hints are provided, but the solution is up to you.

---

## Part 1: Guided Coding

### 1.1 If / Elif / Else

By default, Python runs your code top-to-bottom, one line at a time. An `if` statement lets your program choose between different paths based on a condition.

The structure looks like this:

- `if` — checks a condition. If it's true, run the indented block underneath.
- `elif` — short for "else if." Checked only if the conditions above it were false. You can have as many `elif` branches as you like.
- `else` — the fallback. Runs only if *none* of the conditions above were true.

Let's build a **number checker** that reports whether a number is positive, negative, or zero:

```python
number = 7

if number > 0:
    print("The number is positive.")
elif number < 0:
    print("The number is negative.")
else:
    print("The number is zero.")
```

Run this and you'll see:

```
The number is positive.
```

Walk through what happened:

1. Python evaluated `number > 0`. Since `7 > 0` is `True`, it ran the first block and printed the message.
2. Because the `if` matched, Python **skipped** the `elif` and `else` entirely. Only one branch of an if/elif/else chain ever runs.

Try changing `number` to `-3` and then `0` and re-running. You'll see each branch fire in turn.

**Important:** notice the indentation. Python uses indentation (typically 4 spaces) to know which lines belong to which block. The colon (`:`) at the end of each condition line is also required.

#### Compound conditions

You can combine conditions with `and` and `or`:

- `and` — true only if **both** sides are true
- `or` — true if **either** side is true

Let's extend our checker to also report whether a positive number is small or large:

```python
number = 42

if number > 0 and number < 100:
    print("The number is positive and small (under 100).")
elif number >= 100:
    print("The number is positive and large (100 or more).")
elif number < 0:
    print("The number is negative.")
else:
    print("The number is zero.")
```

Output:

```
The number is positive and small (under 100).
```

Here `number > 0 and number < 100` only passes when *both* comparisons are true. With `number = 42`, both are true, so the first branch runs.

> **Tip:** Python also lets you write `0 < number < 100` as a shorthand for the same thing — but `and`/`or` work everywhere and are worth mastering first.

---

### 1.2 While Loop

A `while` loop repeats a block of code **as long as a condition stays true**. Python checks the condition, runs the block if it's true, then goes back and checks again — over and over until the condition becomes false.

Here's a simple **countdown**:

```python
count = 5

while count > 0:
    print(count)
    count = count - 1

print("Liftoff!")
```

Output:

```
5
4
3
2
1
Liftoff!
```

Walk through what happened:

1. `count` starts at 5. The condition `count > 0` is true, so the loop body runs: it prints `5`, then subtracts 1 so `count` becomes 4.
2. Python checks the condition again. `4 > 0` is still true, so it prints `4` and subtracts again.
3. This continues until `count` reaches 0. Now `count > 0` is **false**, so the loop ends and Python moves on to the line after the loop — printing `Liftoff!`.

**Watch out:** if you forget the line `count = count - 1`, the condition never becomes false and the loop runs forever (an *infinite loop*). If that happens, press `Ctrl+C` in your terminal to stop the program.

> **Shorthand:** `count = count - 1` can also be written `count -= 1`. They do exactly the same thing.

---

### 1.3 For Loop over a List

A `for` loop is the tool of choice when you want to do something **once for each item in a collection**. Unlike a `while` loop, you don't manage a counter yourself — Python hands you each item in turn.

Here we iterate over a list of names:

```python
names = ["Alice", "Bob", "Carmen", "Devi"]

for name in names:
    print("Hello,", name)
```

Output:

```
Hello, Alice
Hello, Bob
Hello, Carmen
Hello, Devi
```

Read the loop line out loud: "for each `name` in `names`..." On each pass through the loop, the variable `name` holds the next item from the list. The loop ends automatically when the list runs out — no condition to manage, no counter to decrement.

#### Getting the index too: `enumerate()`

Sometimes you want the item's *position* as well as the item itself. The built-in `enumerate()` function gives you both at once:

```python
names = ["Alice", "Bob", "Carmen", "Devi"]

for index, name in enumerate(names):
    print(index, name)
```

Output:

```
0 Alice
1 Bob
2 Carmen
3 Devi
```

Each pass through the loop, `enumerate()` hands you a pair: the position (starting at 0, as is standard in Python) and the item. We unpack the pair into two variables, `index` and `name`.

If you'd rather count from 1 — say, for a numbered list shown to humans — pass a starting value:

```python
names = ["Alice", "Bob", "Carmen", "Devi"]

for position, name in enumerate(names, start=1):
    print(position, name)
```

Output:

```
1 Alice
2 Bob
3 Carmen
4 Devi
```

---

### 1.4 For Loop with Range

What if you want to loop a specific number of times, but you don't have a list? The built-in `range()` function generates a sequence of numbers for you.

Let's print the numbers 1 through 10:

```python
for i in range(1, 11):
    print(i)
```

Output:

```
1
2
3
4
5
6
7
8
9
10
```

**Key detail:** `range(1, 11)` starts at 1 and stops *just before* 11. The stop value is never included. This trips up every beginner at least once — if you want 1 through 10, the stop must be 11.

`range()` can take one, two, or three arguments:

- `range(stop)` — starts at 0, counts up to (but not including) `stop`
- `range(start, stop)` — starts at `start`, counts up to (but not including) `stop`
- `range(start, stop, step)` — same, but counts in increments of `step`

Here's all three in action:

```python
# One argument: 0 up to (not including) 5
for i in range(5):
    print(i)        # prints 0, 1, 2, 3, 4

# Two arguments: 2 up to (not including) 6
for i in range(2, 6):
    print(i)        # prints 2, 3, 4, 5

# Three arguments: 0 to 10, stepping by 2
for i in range(0, 11, 2):
    print(i)        # prints 0, 2, 4, 6, 8, 10
```

#### Counting down

A negative step makes `range()` count **down**. Here's our countdown from earlier, rewritten as a `for` loop:

```python
for count in range(5, 0, -1):
    print(count)

print("Liftoff!")
```

Output:

```
5
4
3
2
1
Liftoff!
```

This starts at 5, steps by -1 each time, and stops before reaching 0 — so the last number printed is 1. Compare this with the `while` version from section 1.2: same result, but the `for`/`range()` version manages the counting for you.

---

## Part 2: Exercise — FizzBuzz

Time to put it all together. FizzBuzz is a classic programming exercise that combines a loop with if/elif/else logic — exactly what you've just practiced.

### Your task

Write a program that prints the numbers **1 through 100**, one per line, with three exceptions:

- For multiples of **3**, print `Fizz` instead of the number.
- For multiples of **5**, print `Buzz` instead of the number.
- For multiples of **both 3 and 5**, print `FizzBuzz` instead of the number.

The first 15 lines of correct output look like this:

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
```

### Hint 1: The modulo operator (`%`)

The `%` operator gives you the **remainder** after division. It's the standard way to test whether one number is a multiple of another:

```python
print(10 % 5)   # 0  — 10 divides evenly by 5, no remainder
print(10 % 3)   # 1  — 10 divided by 3 is 3, remainder 1
```

So the test "is `n` a multiple of 3?" is written:

```python
if n % 3 == 0:
    # n is a multiple of 3
```

### Hint 2: Loop structure

You need to visit every number from 1 to 100. A `for` loop with `range()` is a natural fit — remember that the stop value is *not* inclusive, so think carefully about what to pass.

```python
for n in range(...):    # fill in the range
    # your if/elif/else logic here
```

### Hint 3: Order matters

Think about which condition you check **first**. The number 15 is a multiple of 3 *and* a multiple of 5. If your first check is `n % 3 == 0`, then 15 will match it, print `Fizz`, and skip the rest of the chain — and you'll never print `FizzBuzz`. Arrange your conditions so the most specific case is tested before the more general ones.

### Check your work

When you're done, verify against the sample output above. In particular check:

- Line 15 should read `FizzBuzz` (not `Fizz` or `Buzz`)
- Line 100 should read `Buzz`
- Lines 1 and 2 should be plain numbers

Good luck!
