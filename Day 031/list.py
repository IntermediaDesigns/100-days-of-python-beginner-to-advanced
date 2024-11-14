from typing import Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class Node:
    data: Any
    next: Optional["Node"] = None
    prev: Optional["Node"] = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data: Any) -> None:
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def prepend(self, data: Any) -> None:
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def insert_after(self, prev_node: Node, data: Any) -> None:
        if not prev_node:
            return

        new_node = Node(data)
        new_node.next = prev_node.next
        new_node.prev = prev_node
        prev_node.next = new_node

        if new_node.next:
            new_node.next.prev = new_node
        else:
            self.tail = new_node
        self.size += 1

    def delete(self, key: Any) -> None:
        current = self.head

        while current and current.data != key:
            current = current.next

        if not current:
            return

        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next

        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev

        self.size -= 1

    def search(self, key: Any) -> Optional[Node]:
        current = self.head
        while current and current.data != key:
            current = current.next
        return current

    def traverse_forward(self) -> List[Any]:
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def traverse_backward(self) -> List[Any]:
        result = []
        current = self.tail
        while current:
            result.append(current.data)
            current = current.prev
        return result

    def clear(self) -> None:
        self.head = None
        self.tail = None
        self.size = 0


@dataclass
class Task:
    id: int
    title: str
    description: str
    priority: int
    due_date: Optional[datetime] = None
    completed: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        if data["due_date"]:
            data["due_date"] = datetime.fromisoformat(data["due_date"])
        return cls(**data)


class TaskManager:
    def __init__(self):
        self.tasks = DoublyLinkedList()
        self.current_id = 0

    def add_task(
        self,
        title: str,
        description: str,
        priority: int,
        due_date: Optional[datetime] = None,
    ) -> Task:
        self.current_id += 1
        task = Task(self.current_id, title, description, priority, due_date)
        self.tasks.append(task)
        return task

    def delete_task(self, task_id: int) -> None:
        current = self.tasks.head
        while current:
            if current.data.id == task_id:
                self.tasks.delete(current.data)
                break
            current = current.next

    def complete_task(self, task_id: int) -> None:
        task_node = self.find_task(task_id)
        if task_node:
            task_node.data.completed = True

    def find_task(self, task_id: int) -> Optional[Node]:
        current = self.tasks.head
        while current:
            if current.data.id == task_id:
                return current
            current = current.next
        return None

    def get_tasks_by_priority(self) -> List[Task]:
        tasks = []
        current = self.tasks.head
        while current:
            tasks.append(current.data)
            current = current.next
        return sorted(tasks, key=lambda x: (-x.priority, x.due_date or datetime.max))

    def get_pending_tasks(self) -> List[Task]:
        return [task for task in self.tasks.traverse_forward() if not task.completed]

    def get_completed_tasks(self) -> List[Task]:
        return [task for task in self.tasks.traverse_forward() if task.completed]

    def save_tasks(self, filename: str) -> None:
        tasks_data = [task.to_dict() for task in self.tasks.traverse_forward()]
        with open(filename, "w") as f:
            json.dump({"tasks": tasks_data, "current_id": self.current_id}, f, indent=4)

    def load_tasks(self, filename: str) -> None:
        with open(filename, "r") as f:
            data = json.load(f)
            self.tasks.clear()
            self.current_id = data["current_id"]
            for task_data in data["tasks"]:
                task = Task.from_dict(task_data)
                self.tasks.append(task)


def main():
    task_manager = TaskManager()

    while True:
        print("\nTask Manager using Linked List")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Complete Task")
        print("4. View All Tasks")
        print("5. View Tasks by Priority")
        print("6. View Pending Tasks")
        print("7. View Completed Tasks")
        print("8. Save Tasks")
        print("9. Load Tasks")
        print("10. Exit")

        choice = input("\nEnter your choice (1-10): ")

        try:
            if choice == "1":
                title = input("Enter task title: ")
                description = input("Enter task description: ")
                priority = int(input("Enter priority (1-5): "))
                due_date_str = input(
                    "Enter due date (YYYY-MM-DD) or press Enter to skip: "
                )
                due_date = (
                    datetime.strptime(due_date_str, "%Y-%m-%d")
                    if due_date_str
                    else None
                )

                task = task_manager.add_task(title, description, priority, due_date)
                print(f"Task added with ID: {task.id}")

            elif choice == "2":
                task_id = int(input("Enter task ID to delete: "))
                task_manager.delete_task(task_id)
                print("Task deleted successfully!")

            elif choice == "3":
                task_id = int(input("Enter task ID to mark as completed: "))
                task_manager.complete_task(task_id)
                print("Task marked as completed!")

            elif choice == "4":
                print("\nAll Tasks:")
                for task in task_manager.tasks.traverse_forward():
                    print(f"\nID: {task.id}")
                    print(f"Title: {task.title}")
                    print(f"Priority: {task.priority}")
                    print(f"Completed: {'Yes' if task.completed else 'No'}")
                    if task.due_date:
                        print(f"Due Date: {task.due_date.strftime('%Y-%m-%d')}")

            elif choice == "5":
                print("\nTasks by Priority:")
                for task in task_manager.get_tasks_by_priority():
                    print(f"\nID: {task.id}")
                    print(f"Title: {task.title}")
                    print(f"Priority: {task.priority}")
                    print(f"Completed: {'Yes' if task.completed else 'No'}")

            elif choice == "6":
                print("\nPending Tasks:")
                for task in task_manager.get_pending_tasks():
                    print(f"\nID: {task.id}")
                    print(f"Title: {task.title}")
                    print(f"Priority: {task.priority}")
                    if task.due_date:
                        print(f"Due Date: {task.due_date.strftime('%Y-%m-%d')}")

            elif choice == "7":
                print("\nCompleted Tasks:")
                for task in task_manager.get_completed_tasks():
                    print(f"\nID: {task.id}")
                    print(f"Title: {task.title}")
                    print(f"Priority: {task.priority}")

            elif choice == "8":
                filename = input("Enter filename to save tasks: ")
                task_manager.save_tasks(filename)
                print("Tasks saved successfully!")

            elif choice == "9":
                filename = input("Enter filename to load tasks: ")
                task_manager.load_tasks(filename)
                print("Tasks loaded successfully!")

            elif choice == "10":
                print("Thank you for using Task Manager!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
