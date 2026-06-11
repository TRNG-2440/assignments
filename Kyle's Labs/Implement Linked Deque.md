# Advanced Data Structure: Linked List → Deque → Iterable

## Objective
Build a custom data structure from scratch in three phases, progressively adding functionality.

## Setup
Create a new file called `custom_deque.py`.

You will need a `Node` class to hold each element:
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
```

## Phase 1 — Linked List
Create a `LinkedList` class with the following operations:

| Method | Description |
|--------|-------------|
| `__init__()` | Constructor — initialize an empty list |
| `add(value, index=-1)` | Add a value at the given index. Default is end of list |
| `remove(index)` | Remove the element at the given index |
| `replace(index, value)` | Replace the value at the given index |
| `empty()` | Return `True` if the list has no elements |
| `contains(value)` | Check if a value is in the list. Return its index, or `-1` if not found |
| `get(index)` | Return the value at the given index |

### Test Phase 1
```python
ll = LinkedList()
ll.add("a")
ll.add("b")
ll.add("c")
ll.add("x", 1)
print(ll.get(0))       # a
print(ll.get(1))       # x
print(ll.contains("c")) # 3
ll.remove(1)
ll.replace(0, "z")
print(ll.get(0))       # z
print(ll.empty())      # False
```

## Phase 2 — Deque
Extend your `LinkedList` into a `Deque` class (or add methods to the existing class) with the following operations:

| Method | Description |
|--------|-------------|
| `push(value)` | Add to front |
| `pop()` | Remove and return from front |
| `enqueue(value)` | Add to end |
| `dequeue()` | Remove and return from front |
| `peek_front()` | Return the first element without removing it |
| `peek_back()` | Return the last element without removing it |

These should reuse your Phase 1 methods where possible.

### Test Phase 2
```python
dq = Deque()
dq.enqueue("a")
dq.enqueue("b")
dq.enqueue("c")
dq.push("z")
print(dq.peek_front()) # z
print(dq.peek_back())  # c
print(dq.pop())        # z
print(dq.dequeue())    # a
```

## Phase 3 — Make It Iterable
Add the following methods so your deque works with `for` loops and other Python iteration patterns:

| Method | Description |
|--------|-------------|
| `__iter__()` | Return the iterator (usually `self`) and reset traversal |
| `__next__()` | Return the next value, or raise `StopIteration` when done |

### Test Phase 3
```python
dq = Deque()
dq.enqueue("a")
dq.enqueue("b")
dq.enqueue("c")

for item in dq:
    print(item)
# a
# b
# c

print(list(dq))  # ['a', 'b', 'c']
```