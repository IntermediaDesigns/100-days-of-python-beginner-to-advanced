class Book:
    def __init__(self, title, author, isbn, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
        self.available_quantity = quantity

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"


class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.books_borrowed = []

    def __str__(self):
        return f"{self.name} ({self.member_id})"


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Book added: {book}")

    def add_member(self, member):
        self.members.append(member)
        print(f"Member added: {member}")

    def display_books(self):
        if not self.books:
            print("No books in the library.")
            return
        else:
            print("Books in the library:")
            for book in self.books:
                print(f"{book} - {book.available_quantity} available")

    def display_members(self):
        if not self.members:
            print("No members in the library.")
            return
        else:
            print("Members in the library:")
            for member in self.members:
                print(member)

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def find_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def borrow_book(self, member_id, isbn):
        member = self.find_member(member_id)
        if member is None:
            print("Member not found.")
            return
        book = self.find_book(isbn)
        if book is None:
            print("Book not found.")
            return
        if book.available_quantity == 0:
            print("Book not available to borrow.")
            return
        book.available_quantity -= 1
        member.books_borrowed.append(book)
        print(f"{book.title} borrowed by {member}")

    def return_book(self, member_id, isbn):
        member = self.find_member(member_id)
        if member is None:
            print("Member not found.")
            return
        book = self.find_book(isbn)
        if book is None:
            print("Book not found.")
            return
        if book not in member.books_borrowed:
            print("Book not borrowed by member.")
            return

        book.available_quantity += 1
        member.books_borrowed.remove(book)
        print(f"{book.title} returned by {member}")


def main():
    library = Library()

    while True:
        print("\nLibrary Book Management System")
        print("1. Add a book")
        print("2. Add a member")
        print("3. Display all books")
        print("4. Display all members")
        print("5. Borrow a book")
        print("6. Return a book")
        print("7. Exit")
        print()

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            isbn = input("Enter the ISBN of the book: ")
            quantity = int(input("Enter the quantity of the book: "))
            book = Book(title, author, isbn, quantity)
            library.add_book(book)

        elif choice == "2":
            name = input("Enter the name of the member: ")
            member_id = input("Enter the ID of the member: ")
            member = Member(name, member_id)
            library.add_member(member)

        elif choice == "3":
            library.display_books()

        elif choice == "4":
            library.display_members()

        elif choice == "5":
            member_id = input("Enter the ID of the member: ")
            isbn = input("Enter the ISBN of the book: ")
            library.borrow_book(member_id, isbn)

        elif choice == "6":
            member_id = input("Enter the ID of the member: ")
            isbn = input("Enter the ISBN of the book: ")
            library.return_book(member_id, isbn)

        elif choice == "7":
            print("Exiting the Library Book Management System.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
