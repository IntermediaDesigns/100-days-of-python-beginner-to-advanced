import math


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def power(a, b):
    return a**b


def square_root(a):
    if a < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(a)


def get_number_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def calculator():
    operations = {
        "1": ("Addition", add),
        "2": ("Subtraction", subtract),
        "3": ("Multiplication", multiply),
        "4": ("Division", divide),
        "5": ("Power", power),
        "6": ("Square Root", square_root),
    }

    while True:
        print("\nAvailable operations:")
        for key, (name, _) in operations.items():
            print(f"{key}. {name}")
        print("7. Exit")

        choice = input("Enter the number of the operation you want to perform (1-7): ")

        if choice == "7":
            print("Thank you for using the calculator. Goodbye!")
            break

        if choice not in operations:
            print("Invalid choice. Please enter a number from 1 to 7.")
            continue

        operation_name, operation = operations[choice]

        try:
            if choice == "6":
                number = get_number_input(
                    "Enter the number you want to calculate the square root of: "
                )
                result = operation(number)
                print(f"The square root of {number} is: {result}")
            else:
                number1 = get_number_input("Enter the first number: ")
                number2 = get_number_input("Enter the second number: ")
                result = operation(number1, number2)
                print(f"The result of {operation_name} is: {result}")

        except ValueError as e:
            print(f"Error: {e}")

        except ZeroDivisionError:
            print("Cannot divide by zero. Please enter a non-zero number.")

        except OverflowError:
            print("Result is too large. Please enter smaller numbers.")

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    print("Welcome to the calculator with error handling!")
    calculator()
