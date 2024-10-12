import random


def user_guess():

    while True:
        try:
            guess = int(input("Enter your guess: "))
            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100.")
            else:
                return guess
        except ValueError:
            print("Please enter a valid number.")


def play_game(max_attempts):
    secret_number = random.randint(1, 100)
    print("I'm thinking of a number between 1 and 100.")
    print(f"You have {max_attempts} attempts remaining.")

    for attempt in range(1, max_attempts + 1):
        print(f"\nAttempt {attempt} of {max_attempts}")
        guess = user_guess()

        if guess < secret_number:
            print("Too low!")
        elif guess > secret_number:
            print("Too high!")
        else:
            print(f"Congratulations! You guessed the number in {attempt} attempts.")
            return True

    print(f"Sorry, you've run out of attempts. The number was {secret_number}.")
    return False


def main():
    print("Welcome to Guess the Number!")
    global max_attempts
    max_attempts = 7
    games_won = 0
    games_played = 0

    while True:
        games_played += 1
        if play_game(max_attempts):
            games_won += 1

        print(f"\nGames played: {games_played}, Games won: {games_won}")
        print()
        play_again = input("Do you want to play again? (yes/no): ")
        print()
        if play_again.lower() != "yes":
            break

    print("Thanks for playing!")
    print(f"Final score: {games_won} out of {games_played}")


if __name__ == "__main__":
    main()
