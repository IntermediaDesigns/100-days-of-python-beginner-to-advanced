from itertools import islice, tee, chain, takewhile, dropwhile, cycle
from functools import lru_cache, reduce, partial
from typing import Iterator, List, Generator, Optional, Tuple
import time
from dataclasses import dataclass
import matplotlib.pyplot as plt


class FibonacciIterator:
    """Custom Iterator for Fibonacci sequence."""

    def __init__(
        self, max_value: Optional[int] = None, max_length: Optional[int] = None
    ):
        self.max_value = max_value
        self.max_length = max_length
        self.current = 0
        self.next_value = 1
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if (self.max_value and self.current > self.max_value) or (
            self.max_length and self.count >= self.max_length
        ):
            raise StopIteration

        result = self.current
        self.current, self.next_value = self.next_value, self.current + self.next_value
        self.count += 1
        return result


class FibonacciGenerator:
    """Advanced Fibonacci sequence generator with various tools."""

    def __init__(self):
        self.cache = {}

    @staticmethod
    def fibonacci_generator() -> Generator[int, None, None]:
        """Generate Fibonacci numbers using generator."""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    @lru_cache(maxsize=None)
    def fibonacci_recursive(self, n: int) -> int:
        """Calculate nth Fibonacci number using recursion with caching."""
        if n < 2:
            return n
        return self.fibonacci_recursive(n - 1) + self.fibonacci_recursive(n - 2)

    def fibonacci_sequence(self, length: int) -> List[int]:
        """Generate Fibonacci sequence of given length using itertools."""
        return list(islice(self.fibonacci_generator(), length))

    @staticmethod
    def is_fibonacci(num: int) -> bool:
        """Check if a number is in the Fibonacci sequence."""
        perfect_squares = lambda x: x * x == int(x * x)
        return perfect_squares(5 * num * num + 4) or perfect_squares(5 * num * num - 4)

    def get_fibonacci_pairs(self, length: int) -> Iterator[Tuple[int, int]]:
        """Generate pairs of consecutive Fibonacci numbers."""
        sequence = self.fibonacci_generator()
        return zip(sequence, islice(sequence, 1, None))

    def get_golden_ratios(self, length: int) -> Iterator[float]:
        """Calculate golden ratio approximations from Fibonacci pairs."""
        return map(
            lambda pair: pair[1] / pair[0] if pair[0] != 0 else float("inf"),
            self.get_fibonacci_pairs(length),
        )

    def filter_even_fibonacci(self, length: int) -> Iterator[int]:
        """Get even Fibonacci numbers."""
        return filter(lambda x: x % 2 == 0, self.fibonacci_sequence(length))

    def fibonacci_with_indices(self, length: int) -> Iterator[Tuple[int, int]]:
        """Generate Fibonacci numbers with their indices."""
        return enumerate(self.fibonacci_sequence(length))


class FibonacciAnalyzer:
    """Analyze and visualize Fibonacci sequences."""

    @staticmethod
    def analyze_growth_rate(sequence: List[int]) -> List[float]:
        """Calculate growth rate between consecutive numbers."""
        return [
            seq2 / seq1 if seq1 != 0 else float("inf")
            for seq1, seq2 in zip(sequence[:-1], sequence[1:])
        ]

    @staticmethod
    def plot_sequence(sequence: List[int], title: str = "Fibonacci Sequence"):
        """Plot Fibonacci sequence."""
        plt.figure(figsize=(10, 6))
        plt.plot(sequence, marker="o")
        plt.title(title)
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_growth_rate(ratios: List[float]):
        """Plot growth rate convergence to golden ratio."""
        plt.figure(figsize=(10, 6))
        plt.plot(ratios, marker="o")
        plt.axhline(y=(1 + 5**0.5) / 2, color="r", linestyle="--", label="Golden Ratio")
        plt.title("Convergence to Golden Ratio")
        plt.xlabel("Index")
        plt.ylabel("Ratio")
        plt.legend()
        plt.grid(True)
        plt.show()


def main():
    fibonacci_gen = FibonacciGenerator()
    analyzer = FibonacciAnalyzer()

    while True:
        print("\nFibonacci Sequence Generator and Analyzer")
        print("1. Generate Fibonacci Sequence")
        print("2. Check if Number is Fibonacci")
        print("3. Show Golden Ratio Convergence")
        print("4. Show Even Fibonacci Numbers")
        print("5. Analyze Growth Rate")
        print("6. Compare Iterator Performance")
        print("7. Generate Fibonacci Pairs")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ")

        try:
            if choice == "1":
                length = int(input("Enter sequence length: "))
                sequence = fibonacci_gen.fibonacci_sequence(length)
                print("\nFibonacci Sequence:")
                print(sequence)
                plot = input("Plot sequence? (y/n): ").lower() == "y"
                if plot:
                    analyzer.plot_sequence(sequence)

            elif choice == "2":
                num = int(input("Enter a number to check: "))
                if fibonacci_gen.is_fibonacci(num):
                    print(f"{num} is a Fibonacci number!")
                else:
                    print(f"{num} is not a Fibonacci number.")

            elif choice == "3":
                length = int(input("Enter sequence length: "))
                ratios = list(fibonacci_gen.get_golden_ratios(length))
                print("\nGolden Ratio Approximations:")
                for i, ratio in enumerate(ratios, 1):
                    print(f"Step {i}: {ratio}")
                analyzer.plot_growth_rate(ratios)

            elif choice == "4":
                length = int(input("Enter sequence length: "))
                even_fibs = list(fibonacci_gen.filter_even_fibonacci(length))
                print("\nEven Fibonacci Numbers:")
                print(even_fibs)
                plot = input("Plot sequence? (y/n): ").lower() == "y"
                if plot:
                    analyzer.plot_sequence(even_fibs, "Even Fibonacci Numbers")

            elif choice == "5":
                length = int(input("Enter sequence length: "))
                sequence = fibonacci_gen.fibonacci_sequence(length)
                growth_rates = analyzer.analyze_growth_rate(sequence)
                print("\nGrowth Rates:")
                for i, rate in enumerate(growth_rates, 1):
                    print(f"Between steps {i} and {i+1}: {rate}")

            elif choice == "6":
                n = int(input("Enter number for performance comparison: "))

                # Test iterator
                start_time = time.time()
                iterator_result = list(islice(FibonacciIterator(), n))
                iterator_time = time.time() - start_time

                # Test generator
                start_time = time.time()
                generator_result = list(islice(fibonacci_gen.fibonacci_generator(), n))
                generator_time = time.time() - start_time

                # Test recursive with cache
                start_time = time.time()
                recursive_result = [
                    fibonacci_gen.fibonacci_recursive(i) for i in range(n)
                ]
                recursive_time = time.time() - start_time

                print("\nPerformance Comparison:")
                print(f"Iterator Time: {iterator_time:.6f} seconds")
                print(f"Generator Time: {generator_time:.6f} seconds")
                print(f"Recursive (Cached) Time: {recursive_time:.6f} seconds")

            elif choice == "7":
                length = int(input("Enter sequence length: "))
                pairs = list(fibonacci_gen.get_fibonacci_pairs(length))
                print("\nFibonacci Pairs:")
                for i, (a, b) in enumerate(pairs, 1):
                    print(f"Pair {i}: ({a}, {b})")

            elif choice == "8":
                print("Thank you for using the Fibonacci Generator!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
