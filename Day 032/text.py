from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime


class OperationType(Enum):
    INSERT = "insert"
    DELETE = "delete"
    REPLACE = "replace"


@dataclass
class TextOperation:
    type: OperationType
    position: int
    text: str
    old_text: str = ""
    timestamp: datetime = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now()


class TextStack:
    def __init__(self):
        self.items: List[TextOperation] = []

    def push(self, item: TextOperation) -> None:
        self.items.append(item)

    def pop(self) -> Optional[TextOperation]:
        return self.items.pop() if self.items else None

    def peek(self) -> Optional[TextOperation]:
        return self.items[-1] if self.items else None

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def clear(self) -> None:
        self.items.clear()


class TextEditor:
    def __init__(self):
        self.content = ""
        self.undo_stack = TextStack()
        self.redo_stack = TextStack()
        self.save_points: List[str] = []

    def insert(self, position: int, text: str) -> None:
        if 0 <= position <= len(self.content):
            operation = TextOperation(OperationType.INSERT, position, text)
            self.content = self.content[:position] + text + self.content[position:]
            self.undo_stack.push(operation)
            self.redo_stack.clear()

    def delete(self, start: int, end: int) -> None:
        if 0 <= start < end <= len(self.content):
            deleted_text = self.content[start:end]
            operation = TextOperation(OperationType.DELETE, start, "", deleted_text)
            self.content = self.content[:start] + self.content[end:]
            self.undo_stack.push(operation)
            self.redo_stack.clear()

    def replace(self, start: int, end: int, text: str) -> None:
        if 0 <= start < end <= len(self.content):
            old_text = self.content[start:end]
            operation = TextOperation(OperationType.REPLACE, start, text, old_text)
            self.content = self.content[:start] + text + self.content[end:]
            self.undo_stack.push(operation)
            self.redo_stack.clear()

    def undo(self) -> bool:
        operation = self.undo_stack.pop()
        if not operation:
            return False

        if operation.type == OperationType.INSERT:
            pos = operation.position
            length = len(operation.text)
            self.content = self.content[:pos] + self.content[pos + length :]

        elif operation.type == OperationType.DELETE:
            self.content = (
                self.content[: operation.position]
                + operation.old_text
                + self.content[operation.position :]
            )

        elif operation.type == OperationType.REPLACE:
            self.content = (
                self.content[: operation.position]
                + operation.old_text
                + self.content[operation.position + len(operation.text) :]
            )

        self.redo_stack.push(operation)
        return True

    def redo(self) -> bool:
        operation = self.redo_stack.pop()
        if not operation:
            return False

        if operation.type == OperationType.INSERT:
            self.content = (
                self.content[: operation.position]
                + operation.text
                + self.content[operation.position :]
            )

        elif operation.type == OperationType.DELETE:
            end_pos = operation.position + len(operation.old_text)
            self.content = self.content[: operation.position] + self.content[end_pos:]

        elif operation.type == OperationType.REPLACE:
            self.content = (
                self.content[: operation.position]
                + operation.text
                + self.content[operation.position + len(operation.old_text) :]
            )

        self.undo_stack.push(operation)
        return True

    def create_save_point(self) -> None:
        self.save_points.append(self.content)

    def restore_save_point(self, index: int) -> bool:
        if 0 <= index < len(self.save_points):
            self.content = self.save_points[index]
            self.undo_stack.clear()
            self.redo_stack.clear()
            return True
        return False

    def save_to_file(self, filename: str) -> None:
        data = {
            "content": self.content,
            "save_points": self.save_points,
            "timestamp": datetime.now().isoformat(),
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename: str) -> None:
        with open(filename, "r") as f:
            data = json.load(f)
            self.content = data["content"]
            self.save_points = data["save_points"]
            self.undo_stack.clear()
            self.redo_stack.clear()


def main():
    editor = TextEditor()

    while True:
        print("\nText Editor with Undo/Redo")
        print("1. Insert Text")
        print("2. Delete Text")
        print("3. Replace Text")
        print("4. Undo")
        print("5. Redo")
        print("6. View Content")
        print("7. Create Save Point")
        print("8. Restore Save Point")
        print("9. Save to File")
        print("10. Load from File")
        print("11. Exit")

        choice = input("\nEnter choice (1-11): ")

        try:
            if choice == "1":
                position = int(input("Enter position: "))
                text = input("Enter text to insert: ")
                editor.insert(position, text)

            elif choice == "2":
                start = int(input("Enter start position: "))
                end = int(input("Enter end position: "))
                editor.delete(start, end)

            elif choice == "3":
                start = int(input("Enter start position: "))
                end = int(input("Enter end position: "))
                text = input("Enter replacement text: ")
                editor.replace(start, end, text)

            elif choice == "4":
                if editor.undo():
                    print("Undo successful!")
                else:
                    print("Nothing to undo!")

            elif choice == "5":
                if editor.redo():
                    print("Redo successful!")
                else:
                    print("Nothing to redo!")

            elif choice == "6":
                print("\nCurrent Content:")
                print("-" * 50)
                print(editor.content)
                print("-" * 50)

            elif choice == "7":
                editor.create_save_point()
                print(f"Save point {len(editor.save_points)-1} created!")

            elif choice == "8":
                index = int(input("Enter save point index: "))
                if editor.restore_save_point(index):
                    print("Save point restored!")
                else:
                    print("Invalid save point index!")

            elif choice == "9":
                filename = input("Enter filename to save: ")
                editor.save_to_file(filename)
                print("Content saved!")

            elif choice == "10":
                filename = input("Enter filename to load: ")
                editor.load_from_file(filename)
                print("Content loaded!")

            elif choice == "11":
                print("Goodbye!")
                break

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
