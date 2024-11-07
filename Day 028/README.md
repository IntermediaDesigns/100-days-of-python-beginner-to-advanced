# Day 28 Searching algorithms - Mini Project: Binary Search Tree Implementation

![Binary Search](/Day%20028/binary.png)

This project will help you understand BST properties, traversal methods, and searching techniques.

## Key Concepts Demonstrated

### BST Properties
```python
def _insert_recursive(self, node: Node, value: Any) -> Node:
    if value < node.value:
        if node.left is None:
            node.left = Node(value)
        else:
            self._insert_recursive(node.left, value)
```
- Values less than node go left
- Values greater than node go right

### Search Algorithm
```python
def _search_recursive(self, node: Optional[Node], value: Any) -> Optional[Node]:
    if node is None or node.value == value:
        return node
    if value < node.value:
        return self._search_recursive(node.left, value)
    return self._search_recursive(node.right, value)
```
- O(log n) time complexity in balanced trees

### Tree Traversals
```python
def traverse(self, traversal_type: TraversalType) -> Generator[Any, None, None]:
    if traversal_type == TraversalType.INORDER:
        yield from self._inorder_traversal(self.root)
```
- Inorder
- Preorder
- Postorder
- Level-order

### Tree Balancing
```python
def is_balanced(self) -> bool:
    return self._is_balanced_recursive(self.root) != -1
```
- Height difference check
- Balance verification

## Key Features

### Basic Operations
- Insert
- Delete
- Search
- Traversal

### Advanced Features
- Balance checking
- Height calculation
- Visual tree printing
- Operation history

### Persistence
- Save/Load functionality
- Operation logging
- Performance tracking

## To Extend This Project

### Add Support For
- Self-balancing (AVL/Red-Black)
- Range queries
- Custom comparators
- Duplicate values

### Implement
- Tree rotations
