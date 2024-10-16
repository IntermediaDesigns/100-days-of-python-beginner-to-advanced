# Day 11 - Exception handling - Mini Project: Calculator with Error Handling

![Calculator](/Day%20011/calculator.png)

This project will help you practice identifying potential errors, using try-except blocks, and providing user-friendly error messages.

## Key Concepts

### Try-Except Blocks

We use try-except blocks to catch and handle potential errors:
```python
try:
    result = operation(x, y)
except ValueError as e:
    print(f"Error: {e}")
```

### Specific Exception Handling

We catch specific exceptions to provide more precise error messages:
```python
except ValueError as e:
    print(f"Error: {e}")
except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")
except OverflowError:
    print("Error: The result is too large to represent.")
```

### Generic Exception Handling

We use a catch-all exception handler at the end to handle unexpected errors:
```python
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

### Raising Exceptions

We raise custom exceptions in our functions when invalid operations are attempted:
```python
if y == 0:
    raise ValueError("Cannot divide by zero")
```

### Input Validation

We use a separate function with a loop to ensure valid numeric input:
```python
def get_number_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
```

### Handling Multiple Operations

We use a dictionary to store operations, allowing for easy addition of new operations and consistent error handling.

### Graceful Error Recovery

After handling an exception, the program continues running, allowing the user to perform another calculation.

## How to Run This Project

1. Copy the code into a new Python file (e.g., `calculator_with_error_handling.py`).
2. Run the file using Python (e.g., `python calculator_with_error_handling.py` in the command line).
3. Follow the prompts to perform calculations and see how different errors are handled.