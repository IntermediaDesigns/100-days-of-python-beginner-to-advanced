# Day 7 Mini Project: Guess the Number Game

We'll create a Guess the Number game where the computer picks a random number, and the player tries to guess it within a certain number of attempts.

![Guess Number](/Day%20007/guess.png)

## Key Concepts

### While Loops

In the `get_user_guess` function, we use a while loop to continuously prompt the user for input until they provide a valid number:

```python
while True:
    try:
        guess = int(input("Enter your guess: "))
        return guess
    except ValueError:
        print("Invalid input. Please enter a number.")
```

In the main function, we use a while loop to allow the player to play multiple games:

```python
while True:
    # ... (play a game)
    play_again = input("\nDo you want to play again? (yes/no): ").lower()
    if play_again != 'yes':
        # ... (end the game)
        break
```

### For Loops

In the `play_game` function, we use a for loop to manage the number of attempts:

```python
for attempt in range(1, max_attempts + 1):
    print(f"\nAttempt {attempt} of {max_attempts}")
    # ... (handle the guess)
```

### Loop Control

- We use `return` statements inside the for loop in `play_game` to exit the loop early if the player guesses correctly.
- We use a `break` statement in the main game loop to exit when the player chooses not to play again.

### Nested Loops

The while loop in `main` contains the for loop in `play_game`, demonstrating how loops can be nested to create more complex program structures.

### Loop Variables

We use loop variables like `attempt` in the for loop to keep track of the current iteration.

### Infinite Loops with Conditional Breaks

The while loop in `get_user_guess` is an infinite loop that only breaks when valid input is provided.

## Running the Project

1. Copy the code into a new Python file (e.g., `guess_the_number.py`).
2. Run the file using Python (e.g., `python guess_the_number.py` in the command line).
3. Follow the prompts to play rounds of Guess the Number.
