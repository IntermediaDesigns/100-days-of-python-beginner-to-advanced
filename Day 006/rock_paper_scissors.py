def game():
    print("Welcome to Rock Paper Scissors Game!")
    print()
    print("Enter your choice: rock, paper or scissors")
    print()
    user_choice = input()

    print("Your choice is: " + user_choice)
    print()
    import random

    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)
    print("Computer choice is: " + computer_choice)
    print()
    if not user_choice in choices:
        print("Invalid choice! Please enter rock, paper or scissors")
        game()
        print()
    if user_choice == computer_choice:
        print("It's a tie!")
        print()
    elif user_choice == "rock" and computer_choice == "scissors":
        print("You win!")
        print()
    elif user_choice == "paper" and computer_choice == "rock":
        print("You win!")
        print()
    elif user_choice == "scissors" and computer_choice == "paper":
        print("You win!")
        print()
    else:
        print("You lose!")
        print()
    print("Do you want to play again? (yes/no)")
    print()
    play_again = input()
    if play_again == "yes" or play_again == "y":
        game()
    else:
        print("Game Over!")


game()
