# Day 21 Advanced list operations - Mini Project: Inventory Management System

![Inventory](/Day%20021/inventory.png)

# Inventory Management System

This project showcases list comprehensions, sorting, filtering, mapping, and other advanced list manipulation techniques.

## Day 21 Mini Project: Inventory Management System

Let's break down the advanced list operations used in this Inventory Management System:

### List Comprehension:
```python
# Filter products
self.products = [p for p in self.products if p.id != product_id]

# Convert to dict
[p.to_dict() for p in self.products]

# Filter by category
[p for p in self.products if p.category == category]
```

### Filter Function:
```python
list(filter(lambda p: p.quantity <= p.reorder_level, self.products))
```

### Reduce Function:
```python
reduce(lambda acc, p: acc + (p.price * p.quantity), self.products, 0)
```

### Next Function with Generator Expression:
```python
next((p for p in self.products if p.id == product_id), None)
```

### Sorted with Key Function:
```python
sorted(self.products, key=operator.attrgetter(key), reverse=reverse)
```

### Set Comprehension:
```python
self.categories = {p.category for p in self.products}
```

### Any Function:
```python
any(p.id == product.id for p in self.products)
```

## Key Features:

### Product Management:
- Add/Remove products
- Update quantities
- Track low stock

### Search and Filter:
- Search by name/category
- Filter by category
- Sort by various attributes

### Analysis:
- Category summaries
- Total inventory value
- Low stock alerts

### Data Persistence:
- Save/Load functionality
- Transaction history