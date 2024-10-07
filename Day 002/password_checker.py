import re


def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) < 8:
        feedback.append("Password must be at least 8 characters long.")
    else:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Password must contain at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Password must contain at least one lowercase letter.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Password must contain at least one digit.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Password must contain at least one special character.")

    if score == 5:
        strength = "Very Strong"
    elif score == 4:
        strength = "Strong"
    elif score == 3:
        strength = "Moderate"
    elif score == 2:
        strength = "Weak"
    else:
        strength = "Very Weak"

    return strength, feedback


print("Welcome to the Password Strength Checker!")

while True:
    password = input("Enter a password (or 'q' to quit): ")

    if password == "q":
        break

    strength, feedback = check_password_strength(password)

    print(f"Password strength: {strength}")

    if feedback:
        print("Suggestions to improve your password:")
        for suggestion in feedback:
            print(f"- {suggestion}")
    else:
        print("Your password is very strong!")

    print()

print("Goodbye!")
