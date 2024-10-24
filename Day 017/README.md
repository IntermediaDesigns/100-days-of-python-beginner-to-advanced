# Day 17 Context managers - Mini Project: Automated File Backup Tool

![Backup tool](/Day%20017/backup.png)

## Automated File Backup Tool

This project will help you understand how to use both built-in and custom context managers for file handling, directory management, and logging operations.

### Key Concepts of Context Managers

#### Custom Context Manager Class

We create a custom context manager for logging using the class-based approach:

```python
class BackupLogger:
    def __enter__(self):
        # Set up logging
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up logging handlers
```

#### Context Manager Decorator

We use the `@contextmanager` decorator to create a context manager for directory changes:

```python
@contextmanager
def change_dir(destination):
    current_dir = os.getcwd()
    try:
        os.chdir(destination)
        yield
    finally:
        os.chdir(current_dir)
```

#### Built-in Context Managers

We use Python's built-in context managers for file operations:

```python
with open(log_file, 'r') as f:
    print(f.read())
```

#### Nested Context Managers

We demonstrate how to use multiple context managers together:

```python
with BackupLogger(self.log_file) as logger:
    with self.create_backup_zip(backup_path) as zip_file:
        with change_dir(self.source_dir):
            # Perform backup operations
```

#### Resource Management

Context managers ensure proper resource cleanup:

```python
def __exit__(self, exc_type, exc_val, exc_tb):
    # Clean up resources
    for handler in self.logger.handlers[:]:
        handler.close()
        self.logger.removeHandler(handler)
```

#### Exception Handling

Context managers handle exceptions gracefully:

```python
try:
    yield
finally:
    # Cleanup code
```

### To Run This Project

1. Copy the code into a new Python file (e.g., `backup_tool.py`).
2. Run the file using Python (e.g., `python backup_tool.py` in the command line).
3. Follow the prompts to perform backups and view logs.
