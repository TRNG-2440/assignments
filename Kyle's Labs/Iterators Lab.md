# Lab 2: Iterables & Iterators

In Lab 1 you wrote `for` loops over lists and ranges, and they "just worked." In this lab we pull back the curtain: **how** does a `for` loop actually get each item out of a collection? The answer is Python's *iteration protocol* — a simple pair of methods that any object can implement to become loopable.

By the end of this lab you'll understand the machinery well enough to build your **own** objects that work in `for` loops, just like lists do.

This lab has two parts:

1. **Guided Coding** — the theory of iterables and iterators, then a full walkthrough of building an iterable linked list class.
2. **Exercise** — you implement the iteration protocol yourself on a skeleton class.

---

## Part 1: Guided Coding

### 1.1 Theory: Iterables vs. Iterators

Two words that sound almost identical but mean different things:

- An **iterable** is any object you can loop over — a list, a string, a range, a dictionary. Formally: an object that can hand out an *iterator* when asked.
- An **iterator** is the object that does the actual work of producing items, **one at a time**, remembering where it is between requests.

A useful analogy: an iterable is a **book**, and an iterator is a **bookmark**. The book holds the content; the bookmark tracks your current position as you read through it. You can have several bookmarks in the same book, each at a different place — and likewise, you can have several independent iterators over the same iterable.

The protocol comes down to two special methods (Python's special methods are surrounded by double underscores, often pronounced "dunder"):

- `__iter__()` — implemented by the **iterable**. When called, it returns a fresh iterator. ("Give me a bookmark for this book.")
- `__next__()` — implemented by the **iterator**. Each call returns the next item. ("Read the next page and move the bookmark forward.")

When there are no items left, `__next__()` doesn't return some special value — it **raises an exception** called `StopIteration`. That exception is the official signal that iteration is finished.

#### What a for loop really does

When you write:

```python
names = ["Alice", "Bob", "Carmen"]

for name in names:
    print(name)
```

Python performs these steps behind the scenes:

1. Calls `iter(names)`, which calls the list's `__iter__()` method and gets back an **iterator**.
2. Calls `next()` on that iterator, which calls its `__next__()` method, and assigns the result to `name`.
3. Runs the loop body.
4. Repeats steps 2–3 until `__next__()` raises `StopIteration`, at which point the loop ends cleanly. (The `for` loop catches the exception for you — you never see it.)

We can prove this by doing the loop's job **manually**, using the built-in `iter()` and `next()` functions:

```python
names = ["Alice", "Bob", "Carmen"]

it = iter(names)        # Step 1: ask the iterable for an iterator

print(next(it))         # Alice
print(next(it))         # Bob
print(next(it))         # Carmen
print(next(it))         # 💥 raises StopIteration — nothing left!
```

Output:

```
Alice
Bob
Carmen
Traceback (most recent call last):
  ...
StopIteration
```

Notice that the iterator `it` **remembers its position**. Each `next()` call picks up where the last one left off. That's the iterator's whole job: produce the next item, keep track of where you are.

One more detail worth knowing: in Python, iterators are also expected to have an `__iter__()` method that simply returns themselves (`return self`). This means an iterator counts as an iterable too, which is why you can pass an iterator directly to a `for` loop. The bookmark can stand in for the book.

**Summary table:**

| | Iterable | Iterator |
|---|---|---|
| Role | Can be looped over | Produces items one at a time |
| Must implement | `__iter__()` → returns an iterator | `__next__()` → returns next item (and `__iter__()` returning itself) |
| When exhausted | Can hand out a fresh iterator any time | Raises `StopIteration` |
| Examples | list, string, range, dict | the object returned by `iter(...)` |

---

### 1.2 Building an Iterable: A Linked List

Now let's apply the theory. We'll build a **linked list** — a classic data structure — and make it work in a `for` loop by implementing the iteration protocol ourselves.

#### What is a linked list?

A linked list is a chain of small objects called **nodes**. Each node holds two things:

- a **value** (the data)
- a reference to the **next** node in the chain (or `None` if it's the last node)

Unlike a Python list, there's no big block of items in order — just nodes pointing to one another, like a treasure hunt where each clue tells you where the next clue is:

```
head
  ↓
[ "a" | next ] → [ "b" | next ] → [ "c" | None ]
```

#### Step 1: The Node class

Each node is tiny — it just stores a value and a pointer to the next node:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None    # no next node yet
```

#### Step 2: The LinkedList class

The linked list itself only needs to remember the **head** (the first node). We'll also give it an `append()` method to add values to the end of the chain:

```python
class LinkedList:
    def __init__(self):
        self.head = None    # an empty list has no head

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            # The list is empty: the new node becomes the head.
            self.head = new_node
        else:
            # Walk to the end of the chain...
            current = self.head
            while current.next is not None:
                current = current.next
            # ...and attach the new node there.
            current.next = new_node
```

Walk through `append()`:

1. We wrap the value in a fresh `Node`.
2. If the list is empty (`self.head is None`), the new node simply becomes the head.
3. Otherwise we start at the head and follow `.next` pointers until we find the last node (the one whose `.next` is `None`). Note the `while` loop here — flow control from Lab 1, working for us already.
4. We point that last node's `.next` at our new node. The chain grows by one.

#### Step 3: Try to loop over it (and fail)

Let's build a list and try to iterate:

```python
my_list = LinkedList()
my_list.append("a")
my_list.append("b")
my_list.append("c")

for value in my_list:
    print(value)
```

Output:

```
Traceback (most recent call last):
  ...
TypeError: 'LinkedList' object is not iterable
```

Python is telling us exactly what's missing: our class has no `__iter__()` method, so the `for` loop has no way to get an iterator from it. Let's fix that.

#### Step 4: The iterator class

Remember the division of labor: the **iterable** (our `LinkedList`) hands out iterators; the **iterator** tracks a position and produces items. So we write a second class whose only job is to walk the chain:

```python
class LinkedListIterator:
    def __init__(self, start_node):
        self.current = start_node    # the bookmark: where we are now

    def __iter__(self):
        return self                  # an iterator returns itself

    def __next__(self):
        if self.current is None:
            # We've walked off the end of the chain — signal "done."
            raise StopIteration
        value = self.current.value         # grab the value to return
        self.current = self.current.next   # advance the bookmark
        return value
```

Walk through `__next__()` — this is the heart of the whole lab:

1. **Check for the end.** If `self.current` is `None`, we've gone past the last node. We raise `StopIteration` — the official "no more items" signal that `for` loops listen for.
2. **Grab the current value** before we move, so we don't lose it.
3. **Advance the bookmark** by following the `.next` pointer.
4. **Return the value.** The next call to `__next__()` will resume from the new position.

#### Step 5: Connect the iterable to its iterator

Now we add one small method to `LinkedList` so it can hand out iterators. Here's the complete final version of everything:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedListIterator:
    def __init__(self, start_node):
        self.current = start_node

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration
        value = self.current.value
        self.current = self.current.next
        return value


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def __iter__(self):
        # Hand out a fresh iterator that starts at the head.
        return LinkedListIterator(self.head)
```

#### Step 6: Loop over it (and succeed)

```python
my_list = LinkedList()
my_list.append("a")
my_list.append("b")
my_list.append("c")

for value in my_list:
    print(value)
```

Output:

```
a
b
c
```

It works! Trace the full sequence of events one more time, because this is the mental model to take away:

1. The `for` loop calls `iter(my_list)` → our `__iter__()` runs → returns a `LinkedListIterator` positioned at the head node (`"a"`).
2. The loop calls `next()` → `__next__()` returns `"a"` and moves the bookmark to the `"b"` node.
3. `next()` again → returns `"b"`, bookmark moves to `"c"`.
4. `next()` again → returns `"c"`, bookmark moves to `None`.
5. `next()` again → `self.current` is `None` → `StopIteration` is raised → the `for` loop catches it and ends cleanly.

And because `__iter__()` hands out a **fresh** iterator each time it's called, we can loop over the same list twice in a row — each loop gets its own bookmark:

```python
for value in my_list:
    print("first pass:", value)

for value in my_list:
    print("second pass:", value)
```

```
first pass: a
first pass: b
first pass: c
second pass: a
second pass: b
second pass: c
```

---

## Part 2: Exercise — Array Wrapper Object

Now it's your turn to implement the iteration protocol from scratch.

### Your task

Below is a skeleton class called `ArrayWrapper`. It holds a plain Python list internally. Right now, instances of it are **not iterable** — your job is to implement `__iter__()` and `__next__()` so that the test code at the bottom works.

To keep things simple, this exercise uses the common shortcut of making the object **its own iterator**: one class implements both methods, instead of the two-class design we used for the linked list. That means `__iter__()` should return `self` — but it will also need to do one more thing (see Hint 2).

Copy this skeleton into a file and fill in the two methods:

```python
class ArrayWrapper:
    def __init__(self, items):
        self.items = items     # a plain Python list
        self.index = 0         # tracks the current position

    def __iter__(self):
        # TODO: reset the position, then return the iterator.
        pass

    def __next__(self):
        # TODO: if there are no items left, raise StopIteration.
        # Otherwise: grab the item at the current position,
        # advance the position, and return the item.
        pass


# ---- Test code: do not modify below this line ----

wrapper = ArrayWrapper(["red", "green", "blue"])

print("First loop:")
for color in wrapper:
    print(color)

print("Second loop:")
for color in wrapper:
    print(color)
```

### Expected output

```
First loop:
red
green
blue
Second loop:
red
green
blue
```

### Hint 1: The shape of `__next__()`

Your `__next__()` needs to do four things, in this order:

1. Check whether `self.index` has gone past the end of `self.items`. The `len()` function tells you how many items the list holds — and remember that valid indexes run from `0` to `len(self.items) - 1`.
2. If you're past the end, `raise StopIteration`.
3. Otherwise, fetch the item at the current index — `self.items[self.index]` — and store it in a local variable *before* moving on.
4. Add 1 to `self.index`, then return the item you fetched.

This mirrors exactly what `LinkedListIterator.__next__()` did — check for the end, grab the value, advance, return — just with a list index instead of node pointers.

### Hint 2: Why the second loop matters

The test code loops over the same wrapper **twice**. After the first loop finishes, `self.index` has counted all the way past the end. If `__iter__()` only does `return self`, the second loop will start with the position already exhausted and print nothing.

The fix: before returning `self`, have `__iter__()` reset `self.index` back to `0`. The `for` loop always calls `__iter__()` once at the start, so this guarantees every loop begins from the first item.

(This is exactly the trade-off of the "object is its own iterator" shortcut: with the two-class design from the guided section, every loop got a brand-new bookmark automatically. Here we have only one bookmark, so we must rewind it ourselves.)

### Hint 3: Testing without the for loop

If your loop misbehaves, drive the iterator manually to see what's going on — just like we did in the theory section:

```python
wrapper = ArrayWrapper(["red", "green", "blue"])
it = iter(wrapper)
print(next(it))   # should print: red
print(next(it))   # should print: green
print(next(it))   # should print: blue
print(next(it))   # should raise StopIteration
```

### Check your work

- Both loops in the test code print all three colors.
- Calling `next()` a fourth time on a fresh iterator raises `StopIteration` (not an `IndexError`, and not `None`).
- You didn't modify the test code — only the two `TODO` methods.

Good luck!
