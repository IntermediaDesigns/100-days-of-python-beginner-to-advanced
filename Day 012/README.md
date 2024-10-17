# Day 12 - Object-Oriented Programming (OOP) basics - Mini Project: Library Book Management System

![Library Book](/Day%20012/library.png)


This project will help you practice creating classes, objects, and using OOP concepts such as encapsulation and abstraction.

## Day 12 Mini Project: Library Book Management System

Let's break down the key concepts of Object-Oriented Programming used in this Library Book Management System:

### Classes

We define three main classes: `Book`, `Member`, and `Library`. Each class represents a distinct entity in our library system.

### Constructor Method (`__init__`)

Used to initialize object attributes when creating new instances:
```python
def __init__(self, title, author, isbn, quantity):
    self.title = title
    self.author = author
    self.isbn = isbn
    self.quantity = quantity
```

### Instance Attributes

Attributes specific to each instance of a class, e.g., `self.title`, `self.author` in the `Book` class.

### Instance Methods

Methods that operate on instance data, e.g., `add_book`, `borrow_book` in the `Library` class.

### String Representation (`__str__`)

Special method to provide a string representation of objects:
```python
def __str__(self):
    return f"{self.title} by {self.author} (ISBN: {self.isbn})"
```

### Encapsulation

We group related attributes and methods within classes, e.g., all book-related data and operations are in the `Book` class.

### Abstraction

The `Library` class provides a high-level interface for operations like borrowing and returning books, hiding the underlying complexity.

### Object Interactions

Objects of different classes interact with each other, e.g., `Library` manages `Book` and `Member` objects.

### Lists of Objects

The `Library` class maintains lists of `Book` and `Member` objects.

## To run this project

1. Copy the code into a new Python file (e.g., `library_management_system.py`).
2. Run the file using Python (e.g., `python library_management_system.py` in the command line).
3. Follow the prompts to add books and members, borrow and return books, and manage the library system.