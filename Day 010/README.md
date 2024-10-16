# Day 10 - File I/O operations - Mini Project: Personal Diary/Journal

![Diary Journal](/Day%20010/diary.png)

# Personal Diary/Journal

This project will help you practice reading from and writing to files, which are essential skills for data persistence and management in many applications.

## Day 10 Mini Project: Personal Diary/Journal

### Key Concepts

#### File Opening Modes

We use "r" mode for reading and "w" mode for writing:
```python
with open(DIARY_FILE, "r") as file:
    return json.load(file)

with open(DIARY_FILE, "w") as file:
    json.dump(entries, file, indent=4)
```

#### Context Managers (with statement)

We use the `with` statement to ensure files are properly closed after operations:
```python
with open(DIARY_FILE, "r") as file:
    # file operations here
```

#### Reading from Files

We use `json.load()` to read JSON data from the file:
```python
return json.load(file)
```

#### Writing to Files

We use `json.dump()` to write JSON data to the file:
```python
json.dump(entries, file, indent=4)
```

#### Checking File Existence

We use `os.path.exists()` to check if the diary file exists before trying to read from it:
```python
if os.path.exists(DIARY_FILE):
    # file operations here
```

#### File Path Management

We use a constant `DIARY_FILE` to store the file path, making it easy to change if needed.

#### Structured Data Storage

We use JSON format to store diary entries, which allows for easy reading and writing of structured data.

#### Error Handling

While not explicitly shown, the use of `with` statements helps prevent issues with unclosed files.

#### Data Persistence

By saving entries to a file, we ensure that the diary data persists between program runs.

### To Run This Project

1. Copy the code into a new Python file (e.g., `personal_diary.py`).
2. Run the file using Python (e.g., `python personal_diary.py` in the command line).
3. Follow the prompts to add, view, search, or delete diary entries.