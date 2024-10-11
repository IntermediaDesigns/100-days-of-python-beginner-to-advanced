# Day 6 - Conditional statements (if, elif, else) - Mini Project: Rock Paper Scissors Game

![Rock Paper Scissors](/Day%20006/rps.png)

## Key Concepts Related to Conditional Statements

### Basic if-else Structure
- In the `get_user_choice` function, we use a simple if-else structure to validate the user's input:
  ```python
  def get_user_choice():
      choice = input("Enter rock, paper, or scissors: ").lower()
      if choice in ['rock', 'paper', 'scissors']:
          return choice
      print("Invalid choice. Please try again.")
  ```

### Complex Conditional Logic
- In the `determine_winner` function, we use a series of if-elif-else statements to determine the winner:
  ```python
  def determine_winner(user_choice, computer_choice):
      if user_choice == computer_choice:
          return "It's a tie!"
      elif (
          (user_choice == 'rock' and computer_choice == 'scissors') or
          (user_choice == 'paper' and computer_choice == 'rock') or
          (user_choice == 'scissors' and computer_choice == 'paper')
      ):
          return "You win!"
      else:
          return "Computer wins!"
  ```

### Nested Conditionals
- In the main game loop, we use nested conditionals to update the score and check if the player wants to continue:
  ```python
  user_score = 0
  computer_score = 0

  while True:
      user_choice = get_user_choice()
      computer_choice = random.choice(['rock', 'paper', 'scissors'])
      result = determine_winner(user_choice, computer_choice)

      if "You win" in result:
          user_score += 1
      elif "Computer wins" in result:
          computer_score += 1

      print(f"User: {user_score}, Computer: {computer_score}")

      play_again = input("Do you want to play again? (yes/no): ").lower()
      if play_again != 'yes':
          break
  ```

### Boolean Expressions
- We use boolean expressions in our conditionals, such as checking equality (`==`) and membership (`in`).

### Compound Conditions
- In the `determine_winner` function, we use compound conditions with `and` and `or` operators to check for winning conditions.

## To Run This Project
1. Copy the code into a new Python file (e.g., `rock_paper_scissors.py`).
2. Run the file using Python (e.g., `python rock_paper_scissors.py` in the command line).
3. Follow the prompts to play rounds of Rock Paper Scissors against the computer.

