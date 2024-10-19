# Day 13 Mini Project: Bank Account Simulator

![Bank Account](/Day%20013/bank.png)

## Bank Account Simulator

This project will help you practice creating more complex classes with various methods, and show how objects can interact with each other.

### Key Concepts

#### Class Definition

We define several classes: `Transaction`, `BankAccount`, `SavingsAccount`, `CheckingAccount`, and `Bank`. Each class encapsulates related data and methods.

#### Constructor Method (`__init__`)

Used to initialize object attributes when creating new instances:
```python
def __init__(self, account_holder, account_number, initial_balance=0):
    self.account_holder = account_holder
    self.account_number = account_number
    self.balance = initial_balance
```

#### Instance Methods

Methods that operate on instance data, e.g., `deposit`, `withdraw`, `print_statement` in the `BankAccount` class.

#### Class Inheritance

`SavingsAccount` and `CheckingAccount` inherit from `BankAccount`:
```python
class SavingsAccount(BankAccount):
    # ...
```

#### Method Overriding

The `withdraw` method is overridden in `CheckingAccount` to implement overdraft functionality.

#### Super() Function

Used in child classes to call methods from the parent class:
```python
super().__init__(account_holder, account_number, initial_balance)
```

#### Instance Attributes

Attributes specific to each instance, e.g., `self.balance`, `self.transactions`.

#### Class Composition

The `Bank` class contains a dictionary of `BankAccount` objects, demonstrating how objects can contain other objects.

#### Type Checking

We use `isinstance()` to check the type of an account:
```python
if isinstance(account, SavingsAccount):
    # ...
```

#### String Representation (`__str__`)

Implemented in the `Transaction` class to provide a readable string representation of transactions.

### To Run This Project

1. Copy the code into a new Python file (e.g., `bank_account_simulator.py`).
2. Run the file using Python (e.g., `python bank_account_simulator.py` in the command line).
3. Follow the prompts to create accounts, perform transactions, and manage your simulated bank accounts.