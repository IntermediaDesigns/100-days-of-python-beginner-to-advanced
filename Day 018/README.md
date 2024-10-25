# Day 18 Regular expressions - Mini Project: Email and Phone Number Extractor

![Email and Phone](/Day%20018/extractor.png)

This project will help you understand how to use regex patterns to find and validate different types of data in text.

## Key Concepts of Regular Expressions

### Regular Expression Patterns

We define complex patterns for emails and phone numbers:
```python
email_pattern = r'''(?x)       # Flag to allow verbose regex with comments
    ([a-zA-Z0-9._%+-]+)        # Username part
    @                          # @ symbol
    ([a-zA-Z0-9.-]+)          # Domain name
    \.                        # Dot
    ([a-zA-Z]{2,})            # Domain suffix
'''
```

### Regex Flags

We use the `(?x)` flag to allow verbose regex patterns with comments:
```python
re.VERBOSE  # Allows for more readable regex patterns with comments
```

### Pattern Matching

We use various regex functions:
```python
re.finditer()  # Find all matches in text
re.match()     # Check if string matches pattern from start
```

### Grouping

We use parentheses to create capture groups in patterns:
```python
(\d{3})  # Capture group for three digits
```

### Pattern Variations

We handle different phone number formats using multiple patterns:
```python
phone_patterns = {
    'international': r'...',
    'us': r'...',
    'generic': r'...'
}
```

### Pattern Quantifiers

We use various quantifiers in our patterns:
```python
{2,}     # Two or more occurrences
{3,4}    # Three to four occurrences
?        # Zero or one occurrence
```

## How to Run This Project

1. Copy the code into a new Python file (e.g., `data_extractor.py`).
2. Run the file using Python (e.g., `python data_extractor.py` in the command line).
3. Follow the prompts to extract or validate emails and phone numbers.