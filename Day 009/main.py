import random
from quotes_data import quotes
from quote_manager import get_random_quote, add_quote, remove_quote
from user_interface import display_menu, get_user_choice, get_user_input


def main():
    print("Welcome to the Quote of the Day App!")
    print()

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 1:
            quote = get_random_quote(quotes)
            print(f"Here is a random quote for you: {quote}")
            print()
        elif choice == 2:
            new_quote = get_user_input("Enter a new quote: ")
            add_quote(quotes, new_quote)
            print("Quote added successfully!")
            print()
        elif choice == 3:
            quote_to_remove = get_user_input("Enter the quote you want to remove: ")
            remove_quote(quotes, quote_to_remove)
            print("Quote removed successfully!")
            print()
        elif choice == 4:
            print("Thank you for using the Quote of the Day App!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
