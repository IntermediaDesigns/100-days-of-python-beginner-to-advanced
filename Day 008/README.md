# Day 8 Mini Project: Simple Unit Converter

## Simple Unit Converter

This project demonstrates the use of functions and lambda expressions in Python. It will help you practice defining and using functions, as well as understanding the concept of lambda functions for simple, one-time use operations.

### Key Concepts

#### Regular Functions

We define several functions for more complex conversions, e.g.:

```python
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32
```

These functions take one parameter and return the converted value.

#### Lambda Functions

We use lambda functions for simpler, one-line conversions:

```python
meters_to_feet = lambda m: m * 3.28084
```

Lambda functions are anonymous functions that can have any number of arguments but only one expression.

#### Function Documentation

We use docstrings to document what each function does:

```python
def kilometers_to_miles(km):
    """Convert Kilometers to Miles."""
    return km * 0.621371
```

#### Functions as First-Class Objects

We store functions in a dictionary in the `perform_conversion` function, demonstrating that functions can be treated as first-class objects in Python:

```python
conversions = {
    1: (celsius_to_fahrenheit, "°F"),
    # ...
}
```

#### Higher-Order Functions

The `perform_conversion` function takes a function as an argument (stored in the dictionary) and calls it:

```python
func, unit = conversions[choice]
result = func(value)
```

#### Input Validation Function

We create a reusable function `get_numeric_input` to handle and validate user input:

```python
def get_numeric_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
```

#### Main Program Flow

The `main` function orchestrates the overall program flow, calling other functions as needed.

## To Run This Project

1. Copy the code into a new Python file (e.g., `unit_converter.py`).
2. Run the file using Python (e.g., `python unit_converter.py` in the command line).
3. Follow the prompts to perform various unit conversions.
