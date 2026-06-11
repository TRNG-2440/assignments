"""
To-Do List Manager Console Application

This module provides a simple command-line to-do list manager that allows users to:
- Add tasks to a pending list
- View all tasks (pending and completed)
- Mark pending tasks as complete
- Remove completed tasks
- Clear all completed tasks

The application maintains two separate lists to track task states.
"""

from typing import List, Optional


class TodoList:
    def __init__(self) -> None:
        """Initialize the Todo List with empty pending and completed task lists."""
        self.pending_tasks: List[str] = []
        self.completed_tasks: List[str] = []

    def add_task(self, task: str) -> None:
        """
        Add a new task to the pending tasks list.

        Args:
            task: The task description to add.
                  If empty or falsy, no task is added and an error message is printed.
        """
        if task:
            self.pending_tasks.append(task)
            print(f"Task successfully added!: ({self.pending_tasks[-1]})")
        else:
            print("No task description provided! Try again..")

    def view_pending_tasks(self) -> None:
        """Display all pending tasks with their index numbers (1-indexed)."""
        print("Pending Tasks:")
        if len(self.pending_tasks) == 0:
            print("No pending tasks yet.")
        else:
            for idx, task in enumerate(self.pending_tasks):
                print(f"{idx + 1}. {task}")

    def view_completed_tasks(self) -> None:
        """Display all completed tasks with their index numbers (1-indexed)."""
        print("Completed Tasks:")
        if len(self.completed_tasks) == 0:
            print("No completed tasks yet.")
        else:
            for idx, task in enumerate(self.completed_tasks):
                print(f"{idx + 1}. {task}")

    def view_tasks(self) -> None:
        """Display a summary of all tasks (both pending and completed)."""
        print("****************************************")
        print("                SUMMARY                 ")
        print(
            f"Pending tasks: {len(self.pending_tasks)}     Completed tasks: {len(self.completed_tasks)}"
        )
        print("****************************************")

        self.view_pending_tasks()
        print()
        self.view_completed_tasks()

    def complete_task(self, task_id: int) -> None:
        """
        Mark a pending task as complete by moving it to the completed tasks list.

        Args:
            task_id: The 1-indexed position of the task in the pending_tasks list.
                     If invalid, an error message is printed.
        """
        if 1 <= task_id <= len(self.pending_tasks):
            task = self.pending_tasks.pop(task_id - 1)
            self.completed_tasks.append(task)
            print(f"'{self.completed_tasks[-1]}' marked as complete.")
        else:
            print("Invalid task number! Try again..")

    def remove_task(self, task_id: int) -> None:
        """
        Remove a completed task from the completed tasks list.

        Args:
            task_id: The 1-indexed position of the task in the completed_tasks list.
                     If invalid, an error message is printed.
        """
        if 1 <= task_id <= len(self.completed_tasks):
            task = self.completed_tasks.pop(task_id - 1)
            print(f"'{task}' removed from task list.")
        else:
            print("Invalid task number! Try again..")

    def clear_all(self) -> None:
        """Remove all completed tasks from the completed tasks list."""
        self.completed_tasks = []
        print("Cleared all completed tasks")

    @staticmethod
    def print_menu() -> None:
        """Display the main menu options for the to-do list application."""
        print("════════════════════════════════════════")
        print("         TO-DO LIST MANAGER             ")
        print("════════════════════════════════════════")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. Mark a task as complete")
        print("4. Remove a completed task")
        print("5. Clear all completed tasks")
        print("0. Exit")


def try_cast_to_int(prompt: str) -> Optional[int]:
    """
    Prompt the user for input and attempt to convert it to an integer.

    Args:
        prompt: The message to display to the user.

    Returns:
        The integer value if conversion is successful, None if a ValueError occurs.
    """
    input_str: str = input(prompt)
    try:
        return int(input_str)
    except ValueError as e:
        print(f"Error encountered while converting to int: {e}")


if __name__ == "__main__":
    # Initialize the to-do list manager
    manager: TodoList = TodoList()

    # Display the menu once at startup
    manager.print_menu()

    while True:
        print("════════════════════════════════════════")
        selection: Optional[int] = try_cast_to_int(prompt="Select an option: ")

        # Handle user's menu choice
        match selection:
            case 0:
                # Exit the application
                print("Goodbye!")
                break
            case 1:
                # Add a new task
                task: str = input("Enter task: ")
                manager.add_task(task)
            case 2:
                # View all tasks with summary
                manager.view_tasks()
            case 3:
                # Mark a task as complete
                manager.view_pending_tasks()
                task_id: Optional[int] = try_cast_to_int(
                    prompt="Enter task number to complete: "
                )
                if task_id:
                    manager.complete_task(task_id)
            case 4:
                # Remove a completed task
                manager.view_completed_tasks()
                task_id: Optional[int] = try_cast_to_int(
                    prompt="Enter task number to remove: "
                )
                if task_id:
                    manager.remove_task(task_id)
            case 5:
                # Clear all completed tasks
                manager.clear_all()
            case _:
                # Handle invalid menu selections
                print("Invalid choice! Try again..")
                continue
