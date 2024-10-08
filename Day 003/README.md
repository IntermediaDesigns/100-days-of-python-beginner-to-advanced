# Day 3 Lists and list comprehensions - Mini Project: To-Do List Application

This is a simple To-Do List application built using Python. It demonstrates key concepts related to lists and list comprehensions.

![To Do List](/Day%20003/todo.png)

## Key Concepts

### List Initialization

We initialize an empty list `tasks = []` to store our tasks.

### List Operations

- `append()`: We use `tasks.append()` to add new tasks to the list.
- `pop()`: We use `tasks.pop()` to remove tasks from the list.
- **Indexing**: We use indexing (e.g., `tasks[task_num]`) to access specific tasks.

### List of Dictionaries

Each task is stored as a dictionary within the list, allowing us to keep track of both the task description and its completion status.

### List Comprehension

In the `view_tasks()` function, we use a list comprehension to create a formatted list of tasks:

```python
task_list = [f"{i+1}. [{'x' if t['completed'] else ' '}] {t['task']}" 
             for i, t in enumerate(tasks)]
```

This comprehension iterates over the tasks, creating a formatted string for each task including its number, completion status, and description.

### List Methods

- `len()`: We use `len(tasks)` to get the number of tasks in the list.

### Iterating Over Lists

We use `enumerate(tasks)` in the list comprehension to get both the index and value of each task.

## How to Run This Project

1. Copy the code into a new Python file (e.g., `todo_list.py`).
2. Run the file using Python (e.g., `python todo_list.py` in the command line).
3. Follow the prompts to add, view, mark as completed, or remove tasks.