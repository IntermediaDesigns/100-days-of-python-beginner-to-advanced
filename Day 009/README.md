# Day 9 - Modules and packages - Mini Project: Quote of the Day Generator

# Quote of the Day Generator

This project will help you practice importing and using both built-in and custom modules, as well as understanding how to structure your code into reusable components.

![Quote Generator](/Day%20009/quote.png)

## Project Structure

```
quote_generator/
│
├── main.py
├── quotes_data.py
├── quote_manager.py
└── user_interface.py
```

## Files

- **main.py**: Entry point of the application, importing and using functionality from other modules.
- **quotes_data.py**: Contains a list of quotes that can be imported and used in other modules.
- **quote_manager.py**: Handles operations on the quotes list.
- **user_interface.py**: Manages user interaction.

## Key Concepts

### Creating Modules

We've created separate Python files (`quotes_data.py`, `quote_manager.py`, `user_interface.py`) which act as modules. Each module contains related functions and data, promoting code organization and reusability.

### Importing Modules

In `main.py`, we import functions and data from our custom modules:

```python
from quotes_data import quotes
from quote_manager import get_random_quote, add_quote, remove_quote
from user_interface import display_menu, get_user_choice, get_user_input
```

### Importing Built-in Modules

We import the `random` module to select random quotes:

```python
import random
```

### Using Imported Functions

We use functions from our custom modules throughout `main.py`, e.g.:

```python
display_menu()
choice = get_user_choice()
quote, author = get_random_quote(quotes)
```

### Module-level Variables

In `quotes_data.py`, we define a list of quotes that can be imported and used in other modules.

### Encapsulation

Each module encapsulates related functionality:

- `quote_manager.py` handles operations on the quotes list.
- `user_interface.py` manages user interaction.

### Main Script

`main.py` serves as the entry point of our application, importing and using functionality from other modules.

### `if __name__ == "__main__":` Idiom

This idiom in `main.py` ensures that the `main()` function only runs when the script is executed directly, not when it's imported as a module.

## Running the Project

1. Create a new directory named `quote_generator`.
2. Create the four Python files (`main.py`, `quotes_data.py`, `quote_manager.py`, `user_interface.py`) in this directory.
3. Copy the provided code into each respective file.
4. Run the main script using Python (e.g., `python main.py` in the command line from within the `quote_generator` directory).
5. Follow the prompts to get quotes, add new quotes, or remove existing quotes.