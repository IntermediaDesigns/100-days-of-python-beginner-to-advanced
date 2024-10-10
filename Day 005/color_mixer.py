from collections import namedtuple
import random

color = namedtuple("color", ["red", "green", "blue"])


def create_color(red, green, blue):
    """Create a color namedtuple with red, green, and blue values."""
    return color(max(0, min(255, red)), max(0, min(255, green)), max(0, min(255, blue)))


def mix_colors(color1, color2):
    """Mix two colors by averaging their red, green, and blue values."""
    return create_color(
        (color1.red + color2.red) // 2,
        (color1.green + color2.green) // 2,
        (color1.blue + color2.blue) // 2,
    )


def random_color():
    """Create a random color."""
    return create_color(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )


def color_to_hex(color):
    """Convert a color to a hexadecimal string."""
    return "#{:02X}{:02X}{:02X}".format(color.red, color.green, color.blue)


def print_color_info(color):
    """Print information about a color."""
    print(f"RGB: ({color.red}, {color.green}, {color.blue})")
    print(f"Hex: {color_to_hex(color)}")


def main():
    print("Welcome to the RGB Color Mixer!")
    print()

    while True:
        print("\nWhat would you like to do?")
        print("1. Create a random color")
        print("2. Mix two colors")
        print("3. Generate a random color")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            try:
                red = int(input("Enter the red value (0-255): "))
                green = int(input("Enter the green value (0-255): "))
                blue = int(input("Enter the blue value (0-255): "))
                new_color = create_color(red, green, blue)
                print("\nNew color created:")
                print_color_info(new_color)
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "2":
            try:
                print("Enter the values for the first color:")
                red1 = int(input("Red (0-255): "))
                green1 = int(input("Green (0-255): "))
                blue1 = int(input("Blue (0-255): "))
                color1 = create_color(red1, green1, blue1)

                print("Enter the values for the second color:")
                red2 = int(input("Red (0-255): "))
                green2 = int(input("Green (0-255): "))
                blue2 = int(input("Blue (0-255): "))
                color2 = create_color(red2, green2, blue2)

                mixed_color = mix_colors(color1, color2)
                print("\nMixed color:")
                print_color_info(mixed_color)
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "3":
            new_color = random_color()
            print("\nRandom color created:")
            print_color_info(new_color)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
