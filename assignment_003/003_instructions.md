# Python Coding Activity 3 — To-Do List Manager

## Objective

Build a console-based To-Do List Manager that allows a user to add tasks, view all tasks, mark tasks as complete, and remove completed tasks. This activity focuses on **lists** and practices `while` loops, `if-elif-else`, `for` loops, `input()`, and list methods including `append`, `remove`, and indexing.

---

## Background

A list is the natural choice for a to-do list because:

- Tasks are **ordered** — they should appear in the order they were added
- Tasks need to be **added and removed** — lists are mutable
- Tasks need to be **displayed** — lists are easy to loop over

---

## Requirements

### Data

- Maintain two separate lists throughout the program:
  - `pending_tasks` — tasks that have not yet been completed
  - `completed_tasks` — tasks that have been marked as complete

### Menu Options

The program should present the following menu in a loop until the user exits:

```
1. Add a task
2. View all tasks
3. Mark a task as complete
4. Remove a completed task
5. Exit
```

### Feature Instructions

**1. Add a task**
- Prompt the user to enter a task description
- Add the task to the `pending_tasks` list
- Print a confirmation message

**2. View all tasks**
- Display all items in `pending_tasks`, numbered from 1 to n
- Display all items in `completed_tasks`, numbered from 1 to n
- If either list is empty, print a message saying so

**3. Mark a task as complete**
- Display the current `pending_tasks` list, numbered from 1 to n
- Prompt the user to enter the number of the task they want to complete
- Move that task from `pending_tasks` to `completed_tasks`
- Print a confirmation message
- Handle the case where the user enters an invalid number

**4. Remove a completed task**
- Display the current `completed_tasks` list, numbered from 1 to n
- Prompt the user to enter the number of the task they want to remove
- Remove that task from `completed_tasks`
- Print a confirmation message when a task is removed from completed tasks
- Handle the case where the user enters an invalid number

**5. Exit**
- Print a goodbye message and exit the loop

---

## Requirements Checklist

- Two separate lists: `pending_tasks` and `completed_tasks`
- A `while` loop driving the main menu
- Menu selection by entering a valid menu option
- Feature to add new tasks
- Feature to complete tasks
- Feature to delete completed tasks
- Invalid number handling when marking complete or removing a task

---

## Example Interaction

```
════════════════════════════════════════
         TO-DO LIST MANAGER
════════════════════════════════════════
1. Add a task
2. View all tasks
3. Mark a task as complete
4. Remove a completed task
0. Exit
════════════════════════════════════════
Select an option: 1

Enter task: Buy groceries

Task successfully added!: (Buy groceries)

════════════════════════════════════════
Select an option: 2

Pending Tasks:
  1. Buy groceries
  2. Walk the dog

Completed Tasks:
  No completed tasks yet.

════════════════════════════════════════
Select an option: 3

Pending Tasks:
  1. Buy groceries
  2. Walk the dog

Enter task number to complete: 1
'Buy groceries' marked as complete.

════════════════════════════════════════
Select an option: 4

Completed Tasks:
  1. Buy groceries

Enter task number to complete: 1
'Buy groceries' removed from task list.

════════════════════════════════════════
Select an option: 0

Goodbye!
```

---

## Stretch Goals

Once the core program is working, try adding:

- A **"Clear all completed tasks"** option that empties the `completed_tasks` list
- A check that prevents the user from adding an **empty task** (hint: recall truthy/falsy)
- A **task count summary** at the top of the view screen showing how many pending and completed tasks there are