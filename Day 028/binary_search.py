from typing import Optional, List, Any, Generator
from dataclasses import dataclass
from enum import Enum
import json
import time
from collections import deque


class TraversalType(Enum):
    INORDER = "inorder"
    PREORDER = "preorder"
    POSTORDER = "postorder"
    LEVELORDER = "levelorder"


@dataclass
class Node:
    value: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    def to_dict(self) -> dict:
        """Convert node to dictionary for serialization."""
        return {
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
        }


class BinarySearchTree:
    def __init__(self):
        self.root: Optional[Node] = None
        self.comparison_count = 0
        self.operation_history = []

    def reset_counters(self):
        """Reset comparison counter."""
        self.comparison_count = 0

    def insert(self, value: Any) -> None:
        """Insert a value into the BST."""
        start_time = time.time()
        self.reset_counters()

        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

        self._log_operation("insert", value, time.time() - start_time)

    def _insert_recursive(self, node: Node, value: Any) -> Node:
        """Recursive helper method for insertion."""
        self.comparison_count += 1

        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

        return node

    def search(self, value: Any) -> Optional[Node]:
        """Search for a value in the BST."""
        start_time = time.time()
        self.reset_counters()

        result = self._search_recursive(self.root, value)
        self._log_operation("search", value, time.time() - start_time)

        return result

    def _search_recursive(self, node: Optional[Node], value: Any) -> Optional[Node]:
        """Recursive helper method for searching."""
        if node is None or node.value == value:
            self.comparison_count += 1
            return node

        self.comparison_count += 1
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    def delete(self, value: Any) -> None:
        """Delete a value from the BST."""
        start_time = time.time()
        self.reset_counters()

        self.root = self._delete_recursive(self.root, value)
        self._log_operation("delete", value, time.time() - start_time)

    def _delete_recursive(self, node: Optional[Node], value: Any) -> Optional[Node]:
        """Recursive helper method for deletion."""
        if node is None:
            return None

        self.comparison_count += 1
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node with one or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children
            # Get inorder successor (smallest in right subtree)
            temp = self._find_min(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)

        return node

    def _find_min(self, node: Node) -> Node:
        """Find the minimum value node in a subtree."""
        current = node
        while current.left:
            current = current.left
        return current

    def traverse(self, traversal_type: TraversalType) -> Generator[Any, None, None]:
        """Traverse the BST in specified order."""
        if traversal_type == TraversalType.INORDER:
            yield from self._inorder_traversal(self.root)
        elif traversal_type == TraversalType.PREORDER:
            yield from self._preorder_traversal(self.root)
        elif traversal_type == TraversalType.POSTORDER:
            yield from self._postorder_traversal(self.root)
        elif traversal_type == TraversalType.LEVELORDER:
            yield from self._level_order_traversal()

    def _inorder_traversal(self, node: Optional[Node]) -> Generator[Any, None, None]:
        """In-order traversal: Left -> Root -> Right"""
        if node:
            yield from self._inorder_traversal(node.left)
            yield node.value
            yield from self._inorder_traversal(node.right)

    def _preorder_traversal(self, node: Optional[Node]) -> Generator[Any, None, None]:
        """Pre-order traversal: Root -> Left -> Right"""
        if node:
            yield node.value
            yield from self._preorder_traversal(node.left)
            yield from self._preorder_traversal(node.right)

    def _postorder_traversal(self, node: Optional[Node]) -> Generator[Any, None, None]:
        """Post-order traversal: Left -> Right -> Root"""
        if node:
            yield from self._postorder_traversal(node.left)
            yield from self._postorder_traversal(node.right)
            yield node.value

    def _level_order_traversal(self) -> Generator[Any, None, None]:
        """Level-order traversal using queue"""
        if not self.root:
            return

        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            yield node.value

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    def get_height(self) -> int:
        """Get the height of the tree."""
        return self._get_height_recursive(self.root)

    def _get_height_recursive(self, node: Optional[Node]) -> int:
        """Recursive helper method for getting height."""
        if not node:
            return -1
        return (
            max(
                self._get_height_recursive(node.left),
                self._get_height_recursive(node.right),
            )
            + 1
        )

    def is_balanced(self) -> bool:
        """Check if the tree is balanced."""
        return self._is_balanced_recursive(self.root) != -1

    def _is_balanced_recursive(self, node: Optional[Node]) -> int:
        """Recursive helper method for checking balance."""
        if not node:
            return 0

        left_height = self._is_balanced_recursive(node.left)
        if left_height == -1:
            return -1

        right_height = self._is_balanced_recursive(node.right)
        if right_height == -1:
            return -1

        if abs(left_height - right_height) > 1:
            return -1

        return max(left_height, right_height) + 1

    def print_tree(self) -> None:
        """Print tree structure visually."""

        def _build_tree_string(
            node: Optional[Node], prefix: str = "", is_left: bool = True
        ) -> List[str]:
            if not node:
                return []

            lines = []
            value = str(node.value)

            right_lines = _build_tree_string(
                node.right, prefix + ("│   " if is_left else "    "), False
            )
            left_lines = _build_tree_string(
                node.left, prefix + ("│   " if not is_left else "    "), True
            )

            lines.append(prefix + ("└── " if is_left else "┌── ") + value)
            lines.extend(right_lines)
            lines.extend(left_lines)

            return lines

        tree_string = _build_tree_string(self.root, "", True)
        print("\n".join(reversed(tree_string)))

    def _log_operation(self, operation: str, value: Any, time_taken: float) -> None:
        """Log tree operation details."""
        self.operation_history.append(
            {
                "operation": operation,
                "value": value,
                "comparisons": self.comparison_count,
                "time_taken": time_taken,
                "timestamp": time.time(),
            }
        )

    def save_to_file(self, filename: str) -> None:
        """Save tree structure to file."""
        if not self.root:
            data = {"tree": None, "history": self.operation_history}
        else:
            data = {"tree": self.root.to_dict(), "history": self.operation_history}

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename: str) -> None:
        """Load tree structure from file."""

        def dict_to_node(data: dict) -> Optional[Node]:
            if data is None:
                return None
            node = Node(data["value"])
            node.left = dict_to_node(data["left"])
            node.right = dict_to_node(data["right"])
            return node

        with open(filename, "r") as f:
            data = json.load(f)
            self.root = dict_to_node(data["tree"])
            self.operation_history = data["history"]


def main():
    bst = BinarySearchTree()

    while True:
        print("\nBinary Search Tree Operations")
        print("1. Insert Value")
        print("2. Delete Value")
        print("3. Search Value")
        print("4. Traverse Tree")
        print("5. Print Tree")
        print("6. Check Balance")
        print("7. Get Tree Height")
        print("8. Save Tree")
        print("9. Load Tree")
        print("10. View Operation History")
        print("11. Exit")

        choice = input("\nEnter your choice (1-11): ")

        try:
            if choice == "1":
                value = int(input("Enter value to insert: "))
                bst.insert(value)
                print("Value inserted successfully!")
                bst.print_tree()

            elif choice == "2":
                value = int(input("Enter value to delete: "))
                bst.delete(value)
                print("Value deleted successfully!")
                bst.print_tree()

            elif choice == "3":
                value = int(input("Enter value to search: "))
                result = bst.search(value)
                if result:
                    print(f"Value {value} found!")
                else:
                    print(f"Value {value} not found.")
                print(f"Comparisons made: {bst.comparison_count}")

            elif choice == "4":
                print("\nSelect traversal type:")
                print("1. Inorder")
                print("2. Preorder")
                print("3. Postorder")
                print("4. Level-order")

                traversal_choice = input("Enter choice (1-4): ")
                traversal_map = {
                    "1": TraversalType.INORDER,
                    "2": TraversalType.PREORDER,
                    "3": TraversalType.POSTORDER,
                    "4": TraversalType.LEVELORDER,
                }

                if traversal_choice in traversal_map:
                    result = list(bst.traverse(traversal_map[traversal_choice]))
                    print(f"Traversal result: {result}")

            elif choice == "5":
                bst.print_tree()

            elif choice == "6":
                if bst.is_balanced():
                    print("Tree is balanced!")
                else:
                    print("Tree is not balanced.")

            elif choice == "7":
                height = bst.get_height()
                print(f"Tree height: {height}")

            elif choice == "8":
                filename = input("Enter filename to save: ")
                bst.save_to_file(filename)
                print("Tree saved successfully!")

            elif choice == "9":
                filename = input("Enter filename to load: ")
                bst.load_from_file(filename)
                print("Tree loaded successfully!")
                bst.print_tree()

            elif choice == "10":
                print("\nOperation History:")
                for op in bst.operation_history:
                    print(f"Operation: {op['operation']}")
                    print(f"Value: {op['value']}")
                    print(f"Comparisons: {op['comparisons']}")
                    print(f"Time taken: {op['time_taken']:.6f} seconds")
                    print("-" * 30)

            elif choice == "11":
                print("Thank you for using the Binary Search Tree implementation!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
