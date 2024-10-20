# Day 14 Mini Project: Zoo Management System

![Zoo Management](/Day%20014/zoo.png)

## Zoo Management System

This project will help you practice creating class hierarchies, overriding methods, and using polymorphism to handle different types of objects in a unified way.


### Key Concepts

#### Inheritance and Polymorphism

**Abstract Base Class:**

We use the ABC (Abstract Base Class) module to create an abstract `Animal` class:
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    # ...
```

**Abstract Method:**

The `make_sound` method is defined as an abstract method, forcing all subclasses to implement it:
```python
@abstractmethod
def make_sound(self):
    pass
```

**Inheritance:**

We create a hierarchy of classes:
- `Animal` (base class)
  - `Mammal`
    - `Lion`
  - `Bird`
    - `Parrot`
  - `Reptile`
    - `Snake`

Subclasses inherit attributes and methods from their parent classes.

**Method Overriding:**

Subclasses override the `make_sound` method to provide specific implementations:
```python
class Lion(Mammal):
    def make_sound(self):
        return "Roar!"
```

**Polymorphism:**

We treat different animal objects uniformly in methods like `zoo_sounds`:
```python
def zoo_sounds(self):
    for animal in self.animals:
        print(f"{animal.name} the {animal.species} says: {animal.make_sound()}")
```

**Super() Function:**

Used in subclasses to call the constructor of the parent class:
```python
super().__init__(name, age, "Lion", ["meat"], "golden")
```

**Multiple Inheritance Levels:**

`Lion` inherits from `Mammal`, which inherits from `Animal`, demonstrating multi-level inheritance.

**Type Checking:**

We use `isinstance()` to check the type of an animal and perform specific actions:
```python
if isinstance(animal, Mammal):
    animal.groom()
```

**Extending Functionality in Subclasses:**

Subclasses add their own unique methods, like `mimic` for `Parrot`.

### Running the Project

1. Copy the code into a new Python file (e.g., `zoo_management_system.py`).
2. Run the file using Python (e.g., `python zoo_management_system.py` in the command line).
3. Follow the prompts to manage your virtual zoo, adding animals, feeding them, and performing various actions.