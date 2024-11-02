# Day 25 Itertools and functools modules - Mini Project: Custom Iterator for Fibonacci Sequence

![Fibonacci Sequence](/Day%20025/sequence.png)


This project will help you understand how to create custom iterators and use various tools from both modules for sequence manipulation.

## Key Concepts

### itertools:
```python
# Slice iterator
islice(self.fibonacci_generator(), length)

# Create pairs
zip(sequence, islice(sequence, 1, None))

# Chain iterables
chain(iter1, iter2)
```

### functools:
```python
# Cache recursive function
@lru_cache(maxsize=None)

# Partial function application
partial(function, arg)

# Reduce operation
reduce(lambda x, y: x + y, sequence)
```

## Key Features

### Multiple Implementation Methods:
- Custom Iterator
- Generator
- Recursive with caching

### Analysis Tools:
- Growth rate calculation
- Golden ratio convergence
- Performance comparison

### Visualization:
- Sequence plotting
- Growth rate plotting
- Convergence analysis

### Advanced Operations:
- Pair generation
- Filtering
- Sequence manipulation

## Extensions

To extend this project, you could:

### Add support for:
- Different sequence types
- Custom formulas
- Matrix multiplication method
- Big integer support

### Implement:
- Parallel computation
- Memory optimization
- More visualization options
- Sequence comparisons

### Add features for:
- Pattern analysis
- Statistical tools
- Custom sequence rules
- Export capabilities
