contacts = {}


def add_contact():
    name = input("Enter the name of the contact: ")
    if name in contacts:
        print(f"{name} already exists in the contact book.")
        return

    phone = input("Enter the phone number of the contact: ").strip()
    email = input("Enter the email of the contact: ").strip()

    contacts[name] = {"phone": phone, "email": email}
    print(f"{name} has been added to the contact book.")


def view_contact():
    name = input("Enter the name of the contact to view:")
    contact = contacts.get(name)
    if contact:
        print(f"Name: {name}")
        print(f"Phone: {contact['phone']}")
        print(f"Email: {contact['email']}")
    else:
        print(f"{name} does not exist in the contact book.")


def list_contacts():
    if not contacts:
        print("The contact book is empty.")
    else:
        print("\nContacts:")
        for name, info in contacts.items():
            print(f"{name}: {info['phone']}, {info['email']}")


def search_contact():
    term = input("Enter the search term (name, phone, or email): ").strip().lower()
    results = []
    for name, info in contacts.items():
        if (
            term in name.lower()
            or term in info["phone"]
            or term in info["email"].lower()
        ):
            results.append(name)

    if results:
        print("\nMatching contacts:")
        for name in results:
            print(f"{name}: {contacts[name]['phone']}, {contacts[name]['email']}")
    else:
        print(f"No matching contacts found.")


def delete_contact():
    name = input("Enter the name of the contact to delete: ")
    if name in contacts:
        del contacts[name]
        print(f"{name} has been deleted from the contact book.")
    else:
        print(f"{name} does not exist in the contact book.")


def main():
    print("Welcome to the contact book!")

    while True:
        print("\nOptions:")
        print("1. Add contact")
        print("2. View contact")
        print("3. List contacts")
        print("4. Search contacts")
        print("5. Delete contact")
        print("6. Exit")
        print()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contact()
        elif choice == "3":
            list_contacts()
        elif choice == "4":
            search_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
