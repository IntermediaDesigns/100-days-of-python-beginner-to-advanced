from typing import List, Dict, Any, Callable, Iterator
from functools import reduce
from datetime import datetime
import json
import csv
from dataclasses import dataclass
from itertools import groupby
import statistics
import operator


@dataclass
class DataTransformer:
    """Class to handle data transformations using functional programming concepts."""

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """Parse date string to datetime object."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def create_pipeline(*functions: Callable) -> Callable:
        """Create a pipeline of functions to be executed in sequence."""

        def pipeline(data: Any) -> Any:
            return reduce(lambda x, f: f(x), functions, data)

        return pipeline

    @staticmethod
    def filter_by_condition(condition: Callable) -> Callable:
        """Create a filter function based on a condition."""
        return lambda data: list(filter(condition, data))

    @staticmethod
    def map_transform(transform: Callable) -> Callable:
        """Create a map function for transformation."""
        return lambda data: list(map(transform, data))

    @staticmethod
    def reduce_aggregate(operation: Callable) -> Callable:
        """Create a reduce function for aggregation."""
        return lambda data: reduce(operation, data)


class DataProcessor:
    """Class to process and transform data using functional programming."""

    def __init__(self):
        self.transformer = DataTransformer()
        self.transformations: List[Dict[str, Callable]] = []
        self.processed_data: List[Dict] = []

    def load_data(self, filename: str) -> List[Dict]:
        """Load data from JSON or CSV file."""
        if filename.endswith(".json"):
            with open(filename, "r") as f:
                return json.load(f)
        elif filename.endswith(".csv"):
            with open(filename, "r") as f:
                return list(csv.DictReader(f))
        else:
            raise ValueError("Unsupported file format")

    def save_data(self, filename: str, data: List[Dict]) -> None:
        """Save processed data to file."""
        if filename.endswith(".json"):
            with open(filename, "w") as f:
                json.dump(data, f, indent=4, default=str)
        elif filename.endswith(".csv"):
            if data:
                with open(filename, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)

    def add_transformation(self, name: str, transform_func: Callable) -> None:
        """Add a transformation to the pipeline."""
        self.transformations.append(
            {"name": name, "function": transform_func, "timestamp": datetime.now()}
        )

    def process_data(self, data: List[Dict]) -> List[Dict]:
        """Process data through all transformations in the pipeline."""
        processed = data
        for transform in self.transformations:
            processed = transform["function"](processed)
        self.processed_data = processed
        return processed

    def get_transformation_history(self) -> List[Dict]:
        """Get history of applied transformations."""
        return [
            {"name": t["name"], "timestamp": t["timestamp"]}
            for t in self.transformations
        ]


class DataAnalyzer:
    """Class to analyze processed data using functional programming."""

    @staticmethod
    def calculate_statistics(data: List[Dict], field: str) -> Dict:
        """Calculate statistics for a numeric field."""
        values = list(map(lambda x: float(x[field]), data))
        return {
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
        }

    @staticmethod
    def group_by_field(data: List[Dict], field: str) -> Dict:
        """Group data by field value."""
        sorted_data = sorted(data, key=operator.itemgetter(field))
        return {
            key: list(group)
            for key, group in groupby(sorted_data, key=operator.itemgetter(field))
        }

    @staticmethod
    def apply_aggregation(data: List[Dict], field: str, agg_func: Callable) -> Any:
        """Apply aggregation function to a field."""
        return agg_func(map(lambda x: float(x[field]), data))


def main():
    processor = DataProcessor()
    analyzer = DataAnalyzer()

    # Example transformations
    numeric_filter = DataTransformer.filter_by_condition(
        lambda x: all(
            str(v).replace(".", "").isdigit() for v in x.values() if v and v != "N/A"
        )
    )

    round_numbers = DataTransformer.map_transform(
        lambda x: {
            k: round(float(v), 2) if str(v).replace(".", "").isdigit() else v
            for k, v in x.items()
        }
    )

    remove_empty = DataTransformer.filter_by_condition(
        lambda x: all(v for v in x.values())
    )

    while True:
        print("\nData Transformation Pipeline")
        print("1. Load Data")
        print("2. Add Transformation")
        print("3. Process Data")
        print("4. Show Transformation History")
        print("5. Analyze Data")
        print("6. Save Processed Data")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        try:
            if choice == "1":
                filename = input("Enter filename to load: ")
                data = processor.load_data(filename)
                print(f"Loaded {len(data)} records")

            elif choice == "2":
                print("\nAvailable Transformations:")
                print("1. Filter Numeric Values")
                print("2. Round Numbers")
                print("3. Remove Empty Values")
                print("4. Custom Filter")
                print("5. Custom Map")
                print("6. Custom Reduce")

                transform_choice = input("Select transformation (1-6): ")

                if transform_choice == "1":
                    processor.add_transformation("Filter Numeric", numeric_filter)
                elif transform_choice == "2":
                    processor.add_transformation("Round Numbers", round_numbers)
                elif transform_choice == "3":
                    processor.add_transformation("Remove Empty", remove_empty)
                elif transform_choice == "4":
                    field = input("Enter field name: ")
                    value = input("Enter value to filter for: ")
                    custom_filter = DataTransformer.filter_by_condition(
                        lambda x: str(x.get(field)) == value
                    )
                    processor.add_transformation(
                        f"Custom Filter: {field}={value}", custom_filter
                    )
                elif transform_choice == "5":
                    field = input("Enter field name: ")
                    operation = input("Enter operation (+, -, *, /): ")
                    value = float(input("Enter value: "))

                    ops = {
                        "+": operator.add,
                        "-": operator.sub,
                        "*": operator.mul,
                        "/": operator.truediv,
                    }

                    def custom_map(data):
                        return [
                            {
                                **x,
                                field: (
                                    ops[operation](float(x[field]), value)
                                    if str(x[field]).replace(".", "").isdigit()
                                    else x[field]
                                ),
                            }
                            for x in data
                        ]

                    processor.add_transformation(
                        f"Custom Map: {field} {operation} {value}", custom_map
                    )
                elif transform_choice == "6":
                    field = input("Enter field name: ")

                    def custom_reduce(data):
                        values = [
                            float(x[field])
                            for x in data
                            if str(x[field]).replace(".", "").isdigit()
                        ]
                        return [{"sum": sum(values), "count": len(values)}]

                    processor.add_transformation(
                        f"Custom Reduce: Sum {field}", custom_reduce
                    )

            elif choice == "3":
                if not processor.transformations:
                    print("No transformations added!")
                    continue

                processor.process_data(data)
                print(f"Processed {len(processor.processed_data)} records")

            elif choice == "4":
                history = processor.get_transformation_history()
                print("\nTransformation History:")
                for i, t in enumerate(history, 1):
                    print(f"{i}. {t['name']} - {t['timestamp']}")

            elif choice == "5":
                if not processor.processed_data:
                    print("No processed data available!")
                    continue

                print("\nAnalysis Options:")
                print("1. Calculate Statistics")
                print("2. Group By Field")
                print("3. Custom Aggregation")

                analysis_choice = input("Select analysis (1-3): ")
                field = input("Enter field name: ")

                if analysis_choice == "1":
                    stats = analyzer.calculate_statistics(
                        processor.processed_data, field
                    )
                    print("\nStatistics:")
                    for key, value in stats.items():
                        print(f"{key}: {value}")

                elif analysis_choice == "2":
                    groups = analyzer.group_by_field(processor.processed_data, field)
                    print("\nGroups:")
                    for key, group in groups.items():
                        print(f"{key}: {len(group)} records")

                elif analysis_choice == "3":
                    print("\nAggregation Functions:")
                    print("1. Sum")
                    print("2. Average")
                    print("3. Maximum")
                    print("4. Minimum")

                    agg_choice = input("Select function (1-4): ")
                    agg_funcs = {
                        "1": sum,
                        "2": lambda x: sum(x) / len(list(x)),
                        "3": max,
                        "4": min,
                    }

                    if agg_choice in agg_funcs:
                        result = analyzer.apply_aggregation(
                            processor.processed_data, field, agg_funcs[agg_choice]
                        )
                        print(f"\nResult: {result}")

            elif choice == "6":
                if not processor.processed_data:
                    print("No processed data available!")
                    continue

                filename = input("Enter filename to save: ")
                processor.save_data(filename, processor.processed_data)
                print(f"Data saved to {filename}")

            elif choice == "7":
                print("Thank you for using the Data Transformation Pipeline!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
