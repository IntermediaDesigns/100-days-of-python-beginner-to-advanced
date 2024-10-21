# Day 15 Encapsulation and abstraction - Mini Project: Employee Management System

![EMS](/Day%20015/ems.png)

# Employee Management System

This project will help you practice creating classes with private attributes, getter and setter methods, and abstract base classes to enforce a common interface across different types of employees.


### Key Concepts

#### Encapsulation

We use private attributes (denoted by a single underscore) to encapsulate data within classes:
```python
self._emp_id = emp_id
self._name = name
self._email = email
```

Access to these attributes is controlled through getter and setter methods, implemented using the `@property` decorator:
```python
@property
def name(self):
    return self._name

@name.setter
def name(self, value):
    if isinstance(value, str) and len(value) > 0:
        self._name = value
    else:
        raise ValueError("Name must be a non-empty string")
```

#### Abstraction

We use an abstract base class `Employee` to define a common interface for all employee types:
```python
from abc import ABC, abstractmethod

class Employee(ABC):
    # ...
```

The `calculate_salary` method is defined as an abstract method, forcing all subclasses to implement it:
```python
@abstractmethod
def calculate_salary(self):
    pass
```

#### Abstract Base Class

The `Employee` class serves as an abstract base class, providing a blueprint for other employee types.

#### Inheritance

Concrete classes like `Manager`, `Developer`, and `SalesRepresentative` inherit from the abstract `Employee` class.

#### Method Overriding

Each subclass provides its own implementation of the `calculate_salary` method.

#### Data Validation

Setter methods include data validation to ensure the integrity of the object's state:
```python
@salary.setter
def salary(self, value):
    if isinstance(value, (int, float)) and value >= 0:
        self._salary = value
    else:
        raise ValueError("Salary must be a non-negative number")
```

#### Polymorphism

The `EmployeeManagementSystem` class treats all employee types uniformly, demonstrating polymorphism.

### To Run This Project

1. Copy the code into a new Python file (e.g., `employee_management_system.py`).
2. Run the file using Python (e.g., `python employee_management_system.py` in the command line).
3. Follow the prompts to add employees, view their details, calculate salaries, and manage the system.