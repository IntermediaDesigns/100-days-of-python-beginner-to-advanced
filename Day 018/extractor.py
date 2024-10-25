import re
import sys
from typing import List, Tuple, Dict
from datetime import datetime


class DataExtractor:
    def __init__(self):
        # Email regex pattern
        self.email_pattern = r"""(?x)       # Flag to allow verbose regex with comments
            ([a-zA-Z0-9._%+-]+)            # Username part
            @                              # @ symbol
            ([a-zA-Z0-9.-]+)              # Domain name
            \.                            # Dot
            ([a-zA-Z]{2,})                # Domain suffix (e.g., com, org, edu)
        """

        # Phone number regex patterns
        self.phone_patterns = {
            "international": r"""(?x)
                (?:\+|00)                  # '+' or '00' prefix for international
                ([1-9]\d{0,2})             # Country code (1-3 digits)
                [- .]?                     # Optional separator
                (\d{1,3})                  # Area code
                [- .]?                     # Optional separator
                (\d{3,4})                  # First part of number
                [- .]?                     # Optional separator
                (\d{4})                    # Last part of number
            """,
            "us": r"""(?x)
                (?:\+?1[-.]?)?             # Optional US country code
                \(?([0-9]{3})\)?          # Area code with optional parentheses
                [-. ]?                     # Optional separator
                ([0-9]{3})                # First three digits
                [-. ]?                     # Optional separator
                ([0-9]{4})                # Last four digits
            """,
            "generic": r"""(?x)
                (\d{3,4})                  # First part (3-4 digits)
                [- .]?                     # Optional separator
                (\d{3,4})                  # Second part (3-4 digits)
                [- .]?                     # Optional separator
                (\d{4})                    # Last part (4 digits)
            """,
        }

    def extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text."""
        emails = re.finditer(self.email_pattern, text, re.VERBOSE)
        return [match.group(0) for match in emails]

    def extract_phones(self, text: str) -> Dict[str, List[str]]:
        """Extract phone numbers from text and categorize them."""
        phone_numbers = {"international": [], "us": [], "generic": []}

        # Find all matches for each pattern
        for pattern_type, pattern in self.phone_patterns.items():
            matches = re.finditer(pattern, text, re.VERBOSE)
            for match in matches:
                # Format the phone number based on its type
                formatted_number = self.format_phone_number(
                    match.groups(), pattern_type
                )
                if formatted_number not in phone_numbers[pattern_type]:
                    phone_numbers[pattern_type].append(formatted_number)

        return phone_numbers

    def format_phone_number(self, groups: Tuple[str, ...], pattern_type: str) -> str:
        """Format phone numbers based on their type."""
        if pattern_type == "international":
            return f"+{groups[0]} {groups[1]} {groups[2]} {groups[3]}"
        elif pattern_type == "us":
            return f"({groups[0]}) {groups[1]}-{groups[2]}"
        else:  # generic
            return "-".join(groups)

    def validate_email(self, email: str) -> bool:
        """Validate email address format."""
        return bool(re.match(self.email_pattern, email, re.VERBOSE))

    def validate_phone(self, phone: str, pattern_type: str = "generic") -> bool:
        """Validate phone number format."""
        pattern = self.phone_patterns.get(pattern_type, self.phone_patterns["generic"])
        return bool(re.match(pattern, phone, re.VERBOSE))


def save_results(filename: str, emails: List[str], phones: Dict[str, List[str]]):
    """Save extraction results to a file."""
    with open(filename, "w") as f:
        f.write("Extraction Results\n")
        f.write("=================\n")
        f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("Emails Found:\n")
        f.write("-" * 40 + "\n")
        for email in emails:
            f.write(f"{email}\n")

        f.write("\nPhone Numbers Found:\n")
        f.write("-" * 40 + "\n")
        for phone_type, numbers in phones.items():
            if numbers:
                f.write(f"\n{phone_type.title()} Numbers:\n")
                for number in numbers:
                    f.write(f"{number}\n")


def main():
    extractor = DataExtractor()

    while True:
        print("\nEmail and Phone Number Extractor")
        print("================================")
        print("1. Extract from text input")
        print("2. Extract from file")
        print("3. Validate single email")
        print("4. Validate single phone number")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":
            text = input("\nEnter the text to analyze:\n")
            emails = extractor.extract_emails(text)
            phones = extractor.extract_phones(text)

            print("\nResults:")
            print("\nEmails found:")
            for email in emails:
                print(email)

            print("\nPhone numbers found:")
            for phone_type, numbers in phones.items():
                if numbers:
                    print(f"\n{phone_type.title()} Numbers:")
                    for number in numbers:
                        print(number)

            save = input("\nSave results to file? (y/n): ").lower()
            if save == "y":
                filename = (
                    f"extraction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                )
                save_results(filename, emails, phones)
                print(f"Results saved to {filename}")

        elif choice == "2":
            filename = input("Enter the path to the input file: ")
            try:
                with open(filename, "r") as f:
                    text = f.read()
                    emails = extractor.extract_emails(text)
                    phones = extractor.extract_phones(text)

                    output_filename = f"extraction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    save_results(output_filename, emails, phones)
                    print(f"Results saved to {output_filename}")
            except FileNotFoundError:
                print("File not found. Please check the path and try again.")

        elif choice == "3":
            email = input("Enter email to validate: ")
            if extractor.validate_email(email):
                print("Valid email address!")
            else:
                print("Invalid email address!")

        elif choice == "4":
            phone = input("Enter phone number to validate: ")
            print("\nSelect phone number format:")
            print("1. International")
            print("2. US")
            print("3. Generic")

            format_choice = input("Enter choice (1-3): ")
            pattern_type = {"1": "international", "2": "us", "3": "generic"}.get(
                format_choice, "generic"
            )

            if extractor.validate_phone(phone, pattern_type):
                print("Valid phone number!")
            else:
                print("Invalid phone number!")

        elif choice == "5":
            print("Thank you for using the Email and Phone Number Extractor!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
