from typing import List, Tuple, Dict, Callable, Any
import time
import random
from enum import Enum
import matplotlib.pyplot as plt
from dataclasses import dataclass
import json
import math


class AlgorithmType(Enum):
    SORTING = "Sorting"
    SEARCHING = "Searching"
    MATHEMATICAL = "Mathematical"
    DATA_STRUCTURE = "Data Structure"


@dataclass
class AlgorithmInfo:
    """Information about an algorithm."""

    name: str
    type: AlgorithmType
    time_complexity: str
    space_complexity: str
    description: str


class AlgorithmPerformance:
    """Track and analyze algorithm performance."""

    def __init__(self):
        self.execution_times: List[float] = []
        self.input_sizes: List[int] = []
        self.operation_counts: List[int] = []
        self.memory_usage: List[int] = []

    def add_measurement(
        self,
        input_size: int,
        execution_time: float,
        operation_count: int,
        memory_usage: int,
    ):
        """Add a performance measurement."""
        self.input_sizes.append(input_size)
        self.execution_times.append(execution_time)
        self.operation_counts.append(operation_count)
        self.memory_usage.append(memory_usage)

    def get_average_time(self) -> float:
        """Get average execution time."""
        return sum(self.execution_times) / len(self.execution_times)

    def get_worst_time(self) -> float:
        """Get worst execution time."""
        return max(self.execution_times)

    def get_best_time(self) -> float:
        """Get best execution time."""
        return min(self.execution_times)


class AlgorithmAnalyzer:
    """Analyze and compare algorithm performance."""

    def __init__(self):
        self.algorithms: Dict[str, AlgorithmInfo] = {}
        self.performance_data: Dict[str, AlgorithmPerformance] = {}
        self._initialize_algorithms()

    def _initialize_algorithms(self):
        """Initialize available algorithms with their information."""
        # Sorting Algorithms
        self.algorithms["bubble_sort"] = AlgorithmInfo(
            "Bubble Sort",
            AlgorithmType.SORTING,
            "O(n²)",
            "O(1)",
            "Simple sorting algorithm that repeatedly steps through the list, "
            "compares adjacent elements and swaps them if they are in wrong order.",
        )

        self.algorithms["quick_sort"] = AlgorithmInfo(
            "Quick Sort",
            AlgorithmType.SORTING,
            "O(n log n)",
            "O(log n)",
            "Efficient, in-place sorting algorithm that uses divide and conquer strategy.",
        )

        # Searching Algorithms
        self.algorithms["linear_search"] = AlgorithmInfo(
            "Linear Search",
            AlgorithmType.SEARCHING,
            "O(n)",
            "O(1)",
            "Simple search algorithm that checks each element in sequence.",
        )

        self.algorithms["binary_search"] = AlgorithmInfo(
            "Binary Search",
            AlgorithmType.SEARCHING,
            "O(log n)",
            "O(1)",
            "Efficient search algorithm for sorted arrays using divide and conquer.",
        )

        # Mathematical Algorithms
        self.algorithms["fibonacci_recursive"] = AlgorithmInfo(
            "Fibonacci (Recursive)",
            AlgorithmType.MATHEMATICAL,
            "O(2ⁿ)",
            "O(n)",
            "Recursive implementation of Fibonacci sequence calculation.",
        )

        self.algorithms["fibonacci_iterative"] = AlgorithmInfo(
            "Fibonacci (Iterative)",
            AlgorithmType.MATHEMATICAL,
            "O(n)",
            "O(1)",
            "Iterative implementation of Fibonacci sequence calculation.",
        )

    def measure_performance(
        self, algorithm: Callable, input_data: Any, **kwargs
    ) -> Tuple[float, int]:
        """Measure algorithm performance."""
        operation_count = 0
        start_time = time.time()

        # Wrap algorithm execution to count operations
        def count_operations():
            nonlocal operation_count
            operation_count += 1

        result = algorithm(input_data, count_operations, **kwargs)
        execution_time = time.time() - start_time

        return execution_time, operation_count, result

    def run_comparison(
        self, algorithms: List[str], input_sizes: List[int], num_trials: int = 3
    ) -> Dict[str, AlgorithmPerformance]:
        """Run performance comparison for selected algorithms."""
        results = {}

        for algo_name in algorithms:
            if algo_name not in self.algorithms:
                continue

            performance = AlgorithmPerformance()

            for size in input_sizes:
                total_time = 0
                total_ops = 0

                for _ in range(num_trials):
                    # Generate input data based on algorithm type
                    input_data = self._generate_input(algo_name, size)

                    # Get appropriate algorithm implementation
                    algorithm = self._get_algorithm_implementation(algo_name)

                    # Measure performance
                    time_taken, ops_count, _ = self.measure_performance(
                        algorithm, input_data
                    )
                    total_time += time_taken
                    total_ops += ops_count

                # Record average performance
                avg_time = total_time / num_trials
                avg_ops = total_ops / num_trials
                performance.add_measurement(
                    size, avg_time, avg_ops, size * 8
                )  # Approximate memory usage

            results[algo_name] = performance

        return results

    def _generate_input(self, algo_name: str, size: int) -> Any:
        """Generate appropriate input data for given algorithm."""
        if self.algorithms[algo_name].type == AlgorithmType.SORTING:
            return [random.randint(1, 1000) for _ in range(size)]
        elif self.algorithms[algo_name].type == AlgorithmType.SEARCHING:
            data = sorted([random.randint(1, 1000) for _ in range(size)])
            return (data, random.choice(data))  # Return data and search target
        elif self.algorithms[algo_name].type == AlgorithmType.MATHEMATICAL:
            return size
        return None

    def _get_algorithm_implementation(self, algo_name: str) -> Callable:
        """Get the implementation of specified algorithm."""
        implementations = {
            "bubble_sort": self._bubble_sort,
            "quick_sort": self._quick_sort,
            "linear_search": self._linear_search,
            "binary_search": self._binary_search,
            "fibonacci_recursive": self._fibonacci_recursive,
            "fibonacci_iterative": self._fibonacci_iterative,
        }
        return implementations.get(algo_name)

    def _bubble_sort(self, data: List[int], count_op: Callable, **kwargs) -> List[int]:
        """Bubble sort implementation."""
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                count_op()
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def _quick_sort(self, data: List[int], count_op: Callable, **kwargs) -> List[int]:
        """Quick sort implementation."""

        def partition(arr: List[int], low: int, high: int) -> int:
            pivot = arr[high]
            i = low - 1

            for j in range(low, high):
                count_op()
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]

            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        def quick_sort_helper(arr: List[int], low: int, high: int):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort_helper(arr, low, pi - 1)
                quick_sort_helper(arr, pi + 1, high)

        arr = data.copy()
        quick_sort_helper(arr, 0, len(arr) - 1)
        return arr

    def _linear_search(
        self, data: Tuple[List[int], int], count_op: Callable, **kwargs
    ) -> int:
        """Linear search implementation."""
        arr, target = data
        for i, value in enumerate(arr):
            count_op()
            if value == target:
                return i
        return -1

    def _binary_search(
        self, data: Tuple[List[int], int], count_op: Callable, **kwargs
    ) -> int:
        """Binary search implementation."""
        arr, target = data
        left, right = 0, len(arr) - 1

        while left <= right:
            count_op()
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def _fibonacci_recursive(self, n: int, count_op: Callable, **kwargs) -> int:
        """Recursive Fibonacci implementation."""
        count_op()
        if n <= 1:
            return n
        return self._fibonacci_recursive(n - 1, count_op) + self._fibonacci_recursive(
            n - 2, count_op
        )

    def _fibonacci_iterative(self, n: int, count_op: Callable, **kwargs) -> int:
        """Iterative Fibonacci implementation."""
        if n <= 1:
            return n

        a, b = 0, 1
        for _ in range(2, n + 1):
            count_op()
            a, b = b, a + b
        return b

    def plot_comparison(
        self, results: Dict[str, AlgorithmPerformance], plot_type: str = "time"
    ) -> None:
        """Plot performance comparison."""
        plt.figure(figsize=(10, 6))

        for algo_name, performance in results.items():
            if plot_type == "time":
                plt.plot(
                    performance.input_sizes,
                    performance.execution_times,
                    label=self.algorithms[algo_name].name,
                    marker="o",
                )
                plt.ylabel("Execution Time (seconds)")
            elif plot_type == "operations":
                plt.plot(
                    performance.input_sizes,
                    performance.operation_counts,
                    label=self.algorithms[algo_name].name,
                    marker="o",
                )
                plt.ylabel("Operation Count")
            elif plot_type == "memory":
                plt.plot(
                    performance.input_sizes,
                    performance.memory_usage,
                    label=self.algorithms[algo_name].name,
                    marker="o",
                )
                plt.ylabel("Memory Usage (bytes)")

        plt.xlabel("Input Size")
        plt.title(f"Algorithm Comparison ({plot_type.capitalize()})")
        plt.legend()
        plt.grid(True)
        plt.show()

    def save_results(
        self, results: Dict[str, AlgorithmPerformance], filename: str
    ) -> None:
        """Save performance results to file."""
        data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "algorithms": {},
        }

        for algo_name, performance in results.items():
            data["algorithms"][algo_name] = {
                "info": {
                    "name": self.algorithms[algo_name].name,
                    "type": self.algorithms[algo_name].type.value,
                    "time_complexity": self.algorithms[algo_name].time_complexity,
                    "space_complexity": self.algorithms[algo_name].space_complexity,
                },
                "performance": {
                    "input_sizes": performance.input_sizes,
                    "execution_times": performance.execution_times,
                    "operation_counts": performance.operation_counts,
                    "memory_usage": performance.memory_usage,
                },
            }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)


def main():
    analyzer = AlgorithmAnalyzer()

    while True:
        print("\nAlgorithm Comparison Tool")
        print("1. Compare Sorting Algorithms")
        print("2. Compare Searching Algorithms")
        print("3. Compare Mathematical Algorithms")
        print("4. Custom Comparison")
        print("5. View Algorithm Information")
        print("6. Save/Load Results")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        try:
            if choice == "1":
                algorithms = ["bubble_sort", "quick_sort"]
                input_sizes = [100, 500, 1000, 2000, 3000]
                results = analyzer.run_comparison(algorithms, input_sizes)

                print("\nResults:")
                for algo_name, performance in results.items():
                    print(f"\n{analyzer.algorithms[algo_name].name}:")
                    print(f"Average Time: {performance.get_average_time():.6f} seconds")
                    print(f"Best Time: {performance.get_best_time():.6f} seconds")
                    print(f"Worst Time: {performance.get_worst_time():.6f} seconds")

                analyzer.plot_comparison(results, "time")
                analyzer.plot_comparison(results, "operations")

            elif choice == "2":
                algorithms = ["linear_search", "binary_search"]
                input_sizes = [100, 500, 1000, 2000, 3000]
                results = analyzer.run_comparison(algorithms, input_sizes)

                analyzer.plot_comparison(results, "time")
                analyzer.plot_comparison(results, "operations")

            elif choice == "3":
                algorithms = ["fibonacci_recursive", "fibonacci_iterative"]
                input_sizes = [5, 10, 15, 20, 25]
                results = analyzer.run_comparison(algorithms, input_sizes)

                analyzer.plot_comparison(results, "time")
                analyzer.plot_comparison(results, "operations")

            elif choice == "4":
                print("\nAvailable Algorithms:")
                for name, info in analyzer.algorithms.items():
                    print(f"- {name}: {info.name}")

                selected_algos = input(
                    "Enter algorithm names (comma-separated): "
                ).split(",")
                selected_algos = [algo.strip() for algo in selected_algos]

                sizes = input("Enter input sizes (comma-separated): ").split(",")
                input_sizes = [int(size.strip()) for size in sizes]

                results = analyzer.run_comparison(selected_algos, input_sizes)

                plot_types = ["time", "operations", "memory"]
                for plot_type in plot_types:
                    analyzer.plot_comparison(results, plot_type)

            elif choice == "5":
                print("\nAlgorithm Information:")
                for name, info in analyzer.algorithms.items():
                    print(f"\n{info.name}:")
                    print(f"Type: {info.type.value}")
                    print(f"Time Complexity: {info.time_complexity}")
                    print(f"Space Complexity: {info.space_complexity}")
                    print(f"Description: {info.description}")

            elif choice == "6":
                print("\nSelect operation:")
                print("1. Save Results")
                print("2. Load Results")

                op_choice = input("Enter choice (1-2): ")

                if op_choice == "1":
                    filename = input("Enter filename to save results: ")

                    # Run a sample comparison to save
                    print("\nRunning sample comparison...")
                    algorithms = ["bubble_sort", "quick_sort"]
                    input_sizes = [100, 500, 1000]
                    results = analyzer.run_comparison(algorithms, input_sizes)

                    analyzer.save_results(results, filename)
                    print(f"Results saved to {filename}")

                elif op_choice == "2":
                    filename = input("Enter filename to load results: ")
                    try:
                        with open(filename, "r") as f:
                            data = json.load(f)
                            print("\nLoaded Results:")
                            print(f"Timestamp: {data['timestamp']}")
                            for algo_name, algo_data in data["algorithms"].items():
                                print(f"\n{algo_data['info']['name']}:")
                                print(
                                    f"Time Complexity: {algo_data['info']['time_complexity']}"
                                )
                                print(
                                    f"Average Time: {sum(algo_data['performance']['execution_times']) / len(algo_data['performance']['execution_times']):.6f} seconds"
                                )
                    except FileNotFoundError:
                        print("File not found!")
                    except json.JSONDecodeError:
                        print("Invalid file format!")

            elif choice == "7":
                print("Thank you for using the Algorithm Comparison Tool!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
