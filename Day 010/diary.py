import json
import os
from datetime import datetime

DIARY_FILE = "diary_entries.json"


def load_entries():
    """Load diary entries from the JSON file."""
    if os.path.exists(DIARY_FILE):
        with open(DIARY_FILE, "r") as file:
            return json.load(file)
    return {}


def save_entries(entries):
    """Save diary entries to the JSON file."""
    with open(DIARY_FILE, "w") as file:
        json.dump(entries, file, indent=4)


def add_entry(entries):
    """Add a new diary entry."""
    date = datetime.now().strftime("%Y-%m-%d")
    content = input("Enter your diary entry:\n")
    entries[date] = content
    save_entries(entries)
    print("Entry added successfully!")


def view_entries(entries):
    """View all diary entries."""
    if not entries:
        print("No entries found.")
        return
    for index, (date, content) in enumerate(entries.items(), start=1):
        print(f"\nEntry #{index}")
        print(f"Date: {date}")
        print(f"Content: {content}")
        print("-" * 40)


def search_entries(entries):
    """Search for entries containing a specific word."""
    keyword = input("Enter a word to search for: ").lower()
    found_entries = {
        date: content for date, content in entries.items() if keyword in content.lower()
    }

    if found_entries:
        print(f"\nEntries containing '{keyword}':")
        for index, (date, content) in enumerate(found_entries.items(), start=1):
            print(f"\nEntry #{index}")
            print(f"Date: {date}")
            print(f"Content: {content}")
            print("-" * 40)
    else:
        print(f"No entries found containing '{keyword}'.")


def delete_entry(entries):
    """Delete a specific entry by number."""
    if not entries:
        print("No entries found.")
        return

    print("Current entries:")
    entry_list = list(entries.items())
    for index, (date, content) in enumerate(entry_list, start=1):
        preview = content[:50] + "..." if len(content) > 50 else content
        print(f"Entry #{index} - {date}: {preview}")

    try:
        entry_number = int(input("\nEnter the number of the entry to delete: "))
        if 1 <= entry_number <= len(entry_list):
            date_to_delete = entry_list[entry_number - 1][0]
            del entries[date_to_delete]
            save_entries(entries)
            print("Entry deleted successfully!")
        else:
            print("Invalid entry number.")
    except ValueError:
        print("Please enter a valid number.")


def main():
    entries = load_entries()

    while True:
        print("\nPersonal Diary/Journal")
        print("1. Add a new entry")
        print("2. View all entries")
        print("3. Search entries")
        print("4. Delete an entry")
        print("5. Exit")
        print()

        choice = input("Enter your choice (1-5): ")
        print()

        if choice == "1":
            add_entry(entries)
        elif choice == "2":
            view_entries(entries)
        elif choice == "3":
            search_entries(entries)
        elif choice == "4":
            delete_entry(entries)
        elif choice == "5":
            print("Thank you for using the Personal Diary/Journal. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
