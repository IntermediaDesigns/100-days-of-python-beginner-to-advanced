def display_menu():
    print("1. Get a random quote")
    print("2. Add a new quote")
    print("3. Remove a quote")
    print("4. Quit")
    print()

def get_user_choice():
    while True:
        try:
            choice = int(input("Enter your choice: "))
            print()
            return choice
        except ValueError:
            print("Invalid input. Please enter a number.")
            print()


def get_user_input(prompt):
    return input(prompt)
