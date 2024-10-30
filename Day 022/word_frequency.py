import re
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
import json
from pathlib import Path
import string
import matplotlib.pyplot as plt
from datetime import datetime


class WordFrequencyAnalyzer:
    def __init__(self):
        self.word_frequencies: Dict[str, int] = {}
        self.total_words: int = 0
        self.unique_words: int = 0
        self.stop_words: Set[str] = set()
        self.load_stop_words()

    def load_stop_words(self) -> None:
        """Load common stop words from a predefined list."""
        common_stop_words = {
            "the",
            "be",
            "to",
            "of",
            "and",
            "a",
            "in",
            "that",
            "have",
            "i",
            "it",
            "for",
            "not",
            "on",
            "with",
            "he",
            "as",
            "you",
            "do",
            "at",
            "this",
            "but",
            "his",
            "by",
            "from",
            "they",
            "we",
            "say",
            "her",
            "she",
            "or",
            "an",
            "will",
            "my",
            "one",
            "all",
            "would",
            "there",
            "their",
            "what",
            "so",
            "up",
            "out",
            "if",
            "about",
            "who",
            "get",
            "which",
            "go",
            "me",
        }
        self.stop_words = common_stop_words

    def process_text(
        self, text: str, ignore_case: bool = True, ignore_stop_words: bool = True
    ) -> None:
        """Process text and update word frequencies."""
        # Clean and normalize text
        if ignore_case:
            text = text.lower()

        # Remove punctuation and split into words
        words = re.findall(r"\b\w+\b", text)

        # Create frequency dictionary with dictionary comprehension
        word_counts = Counter(
            word
            for word in words
            if not (ignore_stop_words and word in self.stop_words)
        )

        # Update main frequency dictionary
        self.word_frequencies = dict(Counter(self.word_frequencies) + word_counts)

        # Update statistics
        self.total_words = sum(self.word_frequencies.values())
        self.unique_words = len(self.word_frequencies)

    def get_top_words(self, n: int = 10) -> List[Tuple[str, int]]:
        """Get the n most frequent words."""
        return sorted(self.word_frequencies.items(), key=lambda x: (-x[1], x[0]))[:n]

    def get_word_frequency(self, word: str, ignore_case: bool = True) -> int:
        """Get frequency of a specific word."""
        if ignore_case:
            word = word.lower()
            return sum(
                freq for w, freq in self.word_frequencies.items() if w.lower() == word
            )
        return self.word_frequencies.get(word, 0)

    def get_frequency_distribution(self) -> Dict[int, int]:
        """Get distribution of word frequencies."""
        return dict(Counter(self.word_frequencies.values()))

    def get_word_length_distribution(self) -> Dict[int, int]:
        """Get distribution of word lengths."""
        return dict(Counter(len(word) for word in self.word_frequencies.keys()))

    def get_statistics(self) -> Dict[str, float]:
        """Calculate various statistics about the text."""
        return {
            "total_words": self.total_words,
            "unique_words": self.unique_words,
            "average_word_length": sum(
                len(word) * freq for word, freq in self.word_frequencies.items()
            )
            / self.total_words,
            "lexical_diversity": (
                self.unique_words / self.total_words if self.total_words > 0 else 0
            ),
            "most_common_length": max(
                self.get_word_length_distribution().items(), key=lambda x: x[1]
            )[0],
        }

    def save_analysis(self, filename: str) -> None:
        """Save analysis results to a JSON file."""
        analysis = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "statistics": self.get_statistics(),
            "word_frequencies": self.word_frequencies,
            "top_words": dict(self.get_top_words(20)),
            "length_distribution": self.get_word_length_distribution(),
        }

        with open(filename, "w") as f:
            json.dump(analysis, f, indent=4)

    def load_analysis(self, filename: str) -> None:
        """Load analysis results from a JSON file."""
        with open(filename, "r") as f:
            data = json.load(f)
            self.word_frequencies = data["word_frequencies"]
            self.total_words = data["statistics"]["total_words"]
            self.unique_words = data["statistics"]["unique_words"]

    def generate_word_cloud(self, filename: str) -> None:
        """Generate a simple ASCII word cloud."""
        top_words = self.get_top_words(15)
        max_freq = max(freq for _, freq in top_words)

        with open(filename, "w") as f:
            f.write("Word Cloud Visualization\n")
            f.write("=" * 50 + "\n\n")

            for word, freq in top_words:
                # Calculate relative size (1-5 stars)
                stars = int((freq / max_freq) * 5)
                f.write(f"{word.ljust(15)} {'*' * stars} ({freq})\n")


def main():
    analyzer = WordFrequencyAnalyzer()

    while True:
        print("\nWord Frequency Analyzer")
        print("1. Analyze text input")
        print("2. Analyze text file")
        print("3. Show top words")
        print("4. Search word frequency")
        print("5. Show statistics")
        print("6. Generate word cloud")
        print("7. Save analysis")
        print("8. Load analysis")
        print("9. Exit")

        choice = input("\nEnter your choice (1-9): ")

        try:
            if choice == "1":
                text = input("\nEnter text to analyze: ")
                ignore_case = input("Ignore case? (y/n): ").lower() == "y"
                ignore_stop_words = input("Ignore stop words? (y/n): ").lower() == "y"
                analyzer.process_text(text, ignore_case, ignore_stop_words)
                print("Text analyzed successfully!")

            elif choice == "2":
                filename = input("Enter file path: ")
                with open(filename, "r") as f:
                    text = f.read()
                ignore_case = input("Ignore case? (y/n): ").lower() == "y"
                ignore_stop_words = input("Ignore stop words? (y/n): ").lower() == "y"
                analyzer.process_text(text, ignore_case, ignore_stop_words)
                print("File analyzed successfully!")

            elif choice == "3":
                n = int(input("How many top words to show? "))
                print("\nTop Words:")
                for word, freq in analyzer.get_top_words(n):
                    print(f"{word}: {freq}")

            elif choice == "4":
                word = input("Enter word to search: ")
                freq = analyzer.get_word_frequency(word)
                print(f"\nFrequency of '{word}': {freq}")

            elif choice == "5":
                stats = analyzer.get_statistics()
                print("\nText Statistics:")
                for key, value in stats.items():
                    print(f"{key.replace('_', ' ').title()}: {value:.2f}")

            elif choice == "6":
                filename = input("Enter output filename for word cloud: ")
                analyzer.generate_word_cloud(filename)
                print(f"Word cloud saved to {filename}")

            elif choice == "7":
                filename = input("Enter filename to save analysis: ")
                analyzer.save_analysis(filename)
                print("Analysis saved successfully!")

            elif choice == "8":
                filename = input("Enter filename to load analysis: ")
                analyzer.load_analysis(filename)
                print("Analysis loaded successfully!")

            elif choice == "9":
                print("Thank you for using Word Frequency Analyzer!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
