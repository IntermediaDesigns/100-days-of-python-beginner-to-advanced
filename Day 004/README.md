# Day 4 - Dictionaries and sets - Mini Project: Contact Book

# Contact Book Application
![Contact Book](/Day%20004/contact.png)

## Key Concepts

### Dictionary Usage

We use a dictionary `contacts` to store all contacts, where the key is the contact's name and the value is another dictionary containing the contact's information.

**Example:**
```python
contacts = {"John Doe": {"phone": "(123) 456-7890", "email": "john@example.com"}}
```

### Dictionary Methods

- `contacts.get(name)`: Used in `view_contact()` to safely retrieve a contact's information.
- `contacts.items()`: Used in `list_contacts()` and `search_contacts()` to iterate over all contacts.
- `del contacts[name]`: Used in `delete_contact()` to remove a contact.

### Dictionary Operations

- Adding a new key-value pair: `contacts[name] = {"phone": phone, "email": email}`
- Checking if a key exists: `if name in contacts:`

### Nested Dictionaries

Each contact's information is stored as a dictionary within the main `contacts` dictionary.

### Set Usage

In `get_unique_area_codes()`, we use a set to store unique area codes. Sets automatically eliminate duplicates, making them perfect for this use case.

### Set Methods

- `area_codes.add(area_code)`: Adds a new area code to the set.

### Set Operations

We convert the set to a sorted list when displaying area codes: `sorted(area_codes)`

## To Run This Project

1. Copy the code into a new Python file (e.g., `contact_book.py`).
2. Run the file using Python (e.g., `python contact_book.py` in the command line).
3. Follow the prompts to add, view, search, or delete contacts, and to view unique area codes.