tasks = []


def add_task(task):
    tasks.append({"task": task, "completed": False})
    print(f"Task '{task}' added to the list successfully.")


def view_tasks():
    if not tasks:
        print("No tasks in the list.")
    else:
        print("\nCurrent tasks:")
        task_list = [
            f"{i+1}. [{'x' if t['completed'] else ' '}] {t['task']}"
            for i, t in enumerate(tasks)
        ]
        print("\n".join(task_list))


def mark_completed():
    view_tasks()
    if tasks:
        try:
            task_num = int(input("\nEnter the task number to mark as completed: ")) - 1
            if 0 <= task_num < len(tasks):
                tasks[task_num]["completed"] = True
                print(f"Task '{tasks[task_num]['task']}' marked as completed.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid task number.")


def remove_task():
    view_tasks()
    if tasks:
        try:
            task_num = int(input("\nEnter the task number to remove: ")) - 1
            if 0 <= task_num < len(tasks):
                task = tasks.pop(task_num)
                print(f"Task '{task['task']}' removed from the list.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid task number.")


def main():
    print("Welcome to the To-Do List App!")

    while True:
        print("\nWhat would you like to do?")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Mark a task as completed")
        print("4. Remove a task")
        print("5. Exit")
        print()

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            task = input("Enter the task: ")
            add_task(task)

        elif choice == "2":
            view_tasks()

        elif choice == "3":
            mark_completed()

        elif choice == "4":
            remove_task()

        elif choice == "5":
            print("Thank you for using the To-Do List App!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
