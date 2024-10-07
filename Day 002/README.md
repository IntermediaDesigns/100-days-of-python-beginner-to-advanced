# Day 2 of 100

## Strings and String Manipulation - Mini Project: Password Strength Checker

![Password Checker](/Day%20002/password.png)

### Password Strength Checker

**String Length:**
We use `len(password)` to check the length of the password.

**String Methods:**

- `lower()`: Used to convert the input to lowercase when checking for the quit command.

**String Comparison:**
We use `==` to compare strings (e.g., checking if the input is 'q').

**Regular Expressions (regex):**

We use the `re` module to search for patterns in the password.

- `re.search(r"[A-Z]", password)`: Checks for uppercase letters.
- `re.search(r"[a-z]", password)`: Checks for lowercase letters.
- `re.search(r"\d", password)`: Checks for digits.
- `re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)`: Checks for special characters.

**String Formatting:**

We use f-strings (e.g., `f"Password strength: {strength}"`) to format output strings.

**String in List:**
We store feedback messages as strings in a list.

**String Concatenation:**
Implicitly used when adding feedback messages to the list.

### To Run This Project:

1. Copy the code into a new Python file (e.g., `password_checker.py`).
2. Run the file using Python (e.g., `python password_checker.py` in the command line).
3. Enter passwords when prompted to check their strength.
