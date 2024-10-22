import random
import time
from functools import wraps
import json
from datetime import datetime


def timer_decorator(func):
    """Decorator to measure the time taken for each question."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        # Store time taken in the instance rather than the method
        args[0].last_question_time = end_time - start_time
        return result

    return wrapper


def log_performance(func):
    """Decorator to log quiz performance."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        # Load existing log or create new one
        try:
            with open("quiz_log.json", "r") as f:
                log = json.load(f)
        except FileNotFoundError:
            log = []

        # Add new entry using instance attributes
        log.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "score": self.correct_answers,
                "total_questions": self.total_questions,
                "average_time": (
                    self.total_time / self.total_questions
                    if self.total_questions > 0
                    else 0
                ),
            }
        )

        # Save updated log
        with open("quiz_log.json", "w") as f:
            json.dump(log, f, indent=4)

        return result

    return wrapper


def math_problem_generator(difficulty, num_problems):
    """Generator function to create math problems."""
    operations = {
        "easy": ["+", "-"],
        "medium": ["+", "-", "*"],
        "hard": ["+", "-", "*", "/"],
    }

    max_numbers = {"easy": 10, "medium": 50, "hard": 100}

    count = 0
    while count < num_problems:
        op = random.choice(operations[difficulty])
        if op == "/":
            # Ensure division results in whole numbers
            b = random.randint(1, max_numbers[difficulty])
            a = b * random.randint(1, 10)
        else:
            a = random.randint(1, max_numbers[difficulty])
            b = random.randint(1, max_numbers[difficulty])

        if op == "+":
            answer = a + b
        elif op == "-":
            answer = a - b
        elif op == "*":
            answer = a * b
        else:  # op == '/'
            answer = a // b

        yield f"{a} {op} {b}", answer
        count += 1


class MathQuiz:
    def __init__(self):
        self.total_time = 0
        self.correct_answers = 0
        self.total_questions = 0
        self.last_question_time = 0  # New attribute to store last question time

    @timer_decorator
    def ask_question(self, problem, correct_answer):
        """Ask a single question and check the answer."""
        print(f"\nQuestion: What is {problem}?")
        try:
            user_answer = int(input("Your answer: "))
            if user_answer == correct_answer:
                print("Correct!")
                return True
            else:
                print(f"Wrong! The correct answer is {correct_answer}")
                return False
        except ValueError:
            print("Invalid input. Please enter a number.")
            return False

    @log_performance
    def run_quiz(self, difficulty="easy", num_problems=5):
        """Run the complete quiz."""
        print(
            f"\nStarting {difficulty} difficulty quiz with {num_problems} questions..."
        )
        print("=" * 40)

        # Reset statistics for new quiz
        self.total_time = 0
        self.correct_answers = 0
        self.total_questions = num_problems

        # Create generator for math problems
        problems = math_problem_generator(difficulty, num_problems)

        for problem, answer in problems:
            if self.ask_question(problem, answer):
                self.correct_answers += 1
            self.total_time += self.last_question_time

        self.display_results()

    def display_results(self):
        """Display quiz results."""
        print("\nQuiz Results:")
        print("=" * 40)
        print(f"Correct Answers: {self.correct_answers}/{self.total_questions}")
        print(f"Accuracy: {(self.correct_answers/self.total_questions)*100:.1f}%")
        print(
            f"Average Time per Question: {self.total_time/self.total_questions:.2f} seconds"
        )
        print(f"Total Time: {self.total_time:.2f} seconds")


def view_performance_history():
    """View historical quiz performance."""
    try:
        with open("quiz_log.json", "r") as f:
            log = json.load(f)
            print("\nPerformance History:")
            print("=" * 40)
            for entry in log[-5:]:  # Show last 5 entries
                print(f"\nDate: {entry['timestamp']}")
                print(f"Score: {entry['score']}/{entry['total_questions']}")
                print(f"Average Time: {entry['average_time']:.2f} seconds")
    except FileNotFoundError:
        print("\nNo performance history available.")


def main():
    quiz = MathQuiz()

    while True:
        print("\nMath Quiz Game")
        print("1. Start New Quiz")
        print("2. View Performance History")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            print("\nSelect Difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")

            diff_choice = input("Enter your choice (1-3): ")
            difficulty = {"1": "easy", "2": "medium", "3": "hard"}.get(
                diff_choice, "easy"
            )

            num_problems = int(input("How many problems would you like? (1-20): "))
            num_problems = max(1, min(20, num_problems))  # Limit between 1 and 20

            quiz.run_quiz(difficulty, num_problems)

        elif choice == "2":
            view_performance_history()

        elif choice == "3":
            print("\nThanks for playing! Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
