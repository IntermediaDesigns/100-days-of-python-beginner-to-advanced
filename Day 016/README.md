# Day 16 - Decorators and generators - Mini Project: Timed Math Quiz

![quiz](/Day%20016/quiz.png)

## Timed Math Quiz

This project will help you understand how to use decorators to add functionality to functions and how generators can help create sequences of problems efficiently.

### Key Concepts

#### Decorators

We use decorators to add timing and logging functionality:

```python
@timer_decorator
def ask_question(self, problem, correct_answer):
    # ...

@log_performance
def run_quiz(self, difficulty='easy', num_problems=5):
    # ...
```

The `timer_decorator` measures execution time:

```python
def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        wrapper.time_taken = end_time - start_time
        return result
    return wrapper
```

#### Generator Function

We use a generator to create math problems:

```python
def math_problem_generator(difficulty, num_problems):
    # ...
    while count < num_problems:
        # ... generate problem
        yield f"{a} {op} {b}", answer
```

The `yield` keyword makes this a generator function.

#### Decorator Chaining

Multiple decorators can be applied to a single function:

```python
@decorator1
@decorator2
def function():
    # ...
```

#### Generator Usage

We use the generator in a for loop:

```python
for problem, answer in problems:
    # ... handle each problem
```

#### Wrapping Functions

We use `@wraps` from `functools` to preserve function metadata:

```python
from functools import wraps
```

### To Run This Project

1. Copy the code into a new Python file (e.g., `math_quiz.py`).
2. Run the file using Python (e.g., `python math_quiz.py` in the command line).
3. Follow the prompts to take quizzes and view your performance history.