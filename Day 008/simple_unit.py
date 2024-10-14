def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def kilometers_to_miles(kilometers):
    return kilometers * 0.621371


def miles_to_kilometers(miles):
    return miles / 0.621371


meters_to_feet = lambda meters: meters * 3.28084
feet_to_meters = lambda feet: feet / 3.28084

kilograms_to_pounds = lambda kilograms: kilograms * 2.20462
pounds_to_kilograms = lambda pounds: pounds / 2.20462


def get_numeric_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def display_menu():
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Kilometers to Miles")
    print("4. Miles to Kilometers")
    print("5. Meters to Feet")
    print("6. Feet to Meters")
    print("7. Kilograms to Pounds")
    print("8. Pounds to Kilograms")
    print("9. Quit")


def perform_conversion(choice, value):
    conversions = {
        1: (celsius_to_fahrenheit, "°F"),
        2: (fahrenheit_to_celsius, "°C"),
        3: (kilometers_to_miles, "miles"),
        4: (miles_to_kilometers, "km"),
        5: (meters_to_feet, "ft"),
        6: (feet_to_meters, "m"),
        7: (kilograms_to_pounds, "lbs"),
        8: (pounds_to_kilograms, "kg"),
    }

    if choice in conversions:
        func, unit = conversions[choice]
        result = func(value)
        print(f"{value} {unit} is {result:.2f} {unit}")
    else:
        print("Invalid choice")


def main():
    print("Welcome to the Simple Unit Conversion Program")

    while True:
        display_menu()
        choice = get_numeric_input("Enter your choice: ")

        if choice == 9:
            print("Thank you for using the program.")
            break

        if 1 <= choice <= 8:
            value = get_numeric_input("Enter the value: ")
            perform_conversion(int(choice), value)
        else:
            print("Invalid choice. Please select a number from 1 to 9.")


if __name__ == "__main__":
    main()
