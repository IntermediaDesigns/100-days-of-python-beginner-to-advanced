from dataclasses import dataclass
from typing import List, Callable, Dict, Any
import time
import json
from datetime import datetime
import random
import copy


@dataclass
class Track:
    title: str
    artist: str
    album: str
    duration: int  # in seconds
    genre: str
    year: int
    plays: int
    rating: float  # 0-5 stars

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration,
            "genre": self.genre,
            "year": self.year,
            "plays": self.plays,
            "rating": self.rating,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Track":
        return cls(**data)

    def format_duration(self) -> str:
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"


class SortingAlgorithms:
    @staticmethod
    def bubble_sort(
        playlist: List[Track], key_func: Callable, reverse: bool = False
    ) -> List[Track]:
        """Implementation of bubble sort algorithm."""
        n = len(playlist)
        playlist = copy.deepcopy(playlist)

        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if reverse:
                    condition = key_func(playlist[j]) < key_func(playlist[j + 1])
                else:
                    condition = key_func(playlist[j]) > key_func(playlist[j + 1])

                if condition:
                    playlist[j], playlist[j + 1] = playlist[j + 1], playlist[j]
                    swapped = True

            if not swapped:
                break

        return playlist

    @staticmethod
    def quick_sort(
        playlist: List[Track], key_func: Callable, reverse: bool = False
    ) -> List[Track]:
        """Implementation of quick sort algorithm."""
        if len(playlist) <= 1:
            return playlist

        playlist = copy.deepcopy(playlist)
        pivot = playlist[len(playlist) // 2]
        pivot_value = key_func(pivot)

        left = [x for x in playlist if key_func(x) < pivot_value]
        middle = [x for x in playlist if key_func(x) == pivot_value]
        right = [x for x in playlist if key_func(x) > pivot_value]

        if reverse:
            return (
                SortingAlgorithms.quick_sort(right, key_func, reverse)
                + middle
                + SortingAlgorithms.quick_sort(left, key_func, reverse)
            )
        else:
            return (
                SortingAlgorithms.quick_sort(left, key_func, reverse)
                + middle
                + SortingAlgorithms.quick_sort(right, key_func, reverse)
            )

    @staticmethod
    def merge_sort(
        playlist: List[Track], key_func: Callable, reverse: bool = False
    ) -> List[Track]:
        """Implementation of merge sort algorithm."""
        if len(playlist) <= 1:
            return playlist

        playlist = copy.deepcopy(playlist)
        mid = len(playlist) // 2
        left = SortingAlgorithms.merge_sort(playlist[:mid], key_func, reverse)
        right = SortingAlgorithms.merge_sort(playlist[mid:], key_func, reverse)

        return SortingAlgorithms.merge(left, right, key_func, reverse)

    @staticmethod
    def merge(
        left: List[Track], right: List[Track], key_func: Callable, reverse: bool
    ) -> List[Track]:
        """Helper function for merge sort."""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if reverse:
                condition = key_func(left[i]) > key_func(right[j])
            else:
                condition = key_func(left[i]) < key_func(right[j])

            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result


class PlaylistManager:
    def __init__(self):
        self.playlist: List[Track] = []
        self.sorting_algorithms = {
            "bubble": SortingAlgorithms.bubble_sort,
            "quick": SortingAlgorithms.quick_sort,
            "merge": SortingAlgorithms.merge_sort,
        }
        self.sort_history: List[Dict] = []

    def add_track(self, track: Track) -> None:
        """Add a track to the playlist."""
        self.playlist.append(track)

    def get_key_function(self, sort_by: str) -> Callable:
        """Get the key function for sorting."""
        key_functions = {
            "title": lambda x: x.title.lower(),
            "artist": lambda x: x.artist.lower(),
            "album": lambda x: x.album.lower(),
            "duration": lambda x: x.duration,
            "genre": lambda x: x.genre.lower(),
            "year": lambda x: x.year,
            "plays": lambda x: x.plays,
            "rating": lambda x: x.rating,
        }
        return key_functions.get(sort_by, lambda x: x.title.lower())

    def sort_playlist(
        self, sort_by: str, algorithm: str = "quick", reverse: bool = False
    ) -> List[Track]:
        """Sort the playlist using specified algorithm and criteria."""
        start_time = time.time()

        key_func = self.get_key_function(sort_by)
        sort_func = self.sorting_algorithms.get(
            algorithm, self.sorting_algorithms["quick"]
        )

        sorted_playlist = sort_func(self.playlist, key_func, reverse)

        end_time = time.time()
        execution_time = end_time - start_time

        # Record sorting history
        self.sort_history.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "algorithm": algorithm,
                "criteria": sort_by,
                "reverse": reverse,
                "execution_time": execution_time,
                "playlist_size": len(self.playlist),
            }
        )

        return sorted_playlist

    def save_playlist(self, filename: str) -> None:
        """Save playlist to a JSON file."""
        data = {
            "tracks": [track.to_dict() for track in self.playlist],
            "sort_history": self.sort_history,
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_playlist(self, filename: str) -> None:
        """Load playlist from a JSON file."""
        with open(filename, "r") as f:
            data = json.load(f)
            self.playlist = [Track.from_dict(track) for track in data["tracks"]]
            self.sort_history = data.get("sort_history", [])

    def get_sorting_performance(self) -> Dict[str, float]:
        """Compare performance of different sorting algorithms."""
        results = {}
        test_data = copy.deepcopy(self.playlist)
        key_func = lambda x: x.title.lower()

        for algorithm in self.sorting_algorithms:
            start_time = time.time()
            self.sorting_algorithms[algorithm](test_data, key_func)
            execution_time = time.time() - start_time
            results[algorithm] = execution_time

        return results


def generate_sample_playlist(size: int) -> List[Track]:
    """Generate sample playlist for testing."""
    genres = ["Rock", "Pop", "Jazz", "Classical", "Hip Hop", "Electronic"]
    artists = ["Artist A", "Artist B", "Artist C", "Artist D", "Artist E"]
    albums = ["Album 1", "Album 2", "Album 3", "Album 4", "Album 5"]

    return [
        Track(
            title=f"Track {i}",
            artist=random.choice(artists),
            album=random.choice(albums),
            duration=random.randint(120, 480),
            genre=random.choice(genres),
            year=random.randint(1970, 2023),
            plays=random.randint(0, 1000),
            rating=round(random.uniform(1, 5), 1),
        )
        for i in range(1, size + 1)
    ]


def main():
    manager = PlaylistManager()

    while True:
        print("\nMusic Playlist Sorter")
        print("1. Add Track")
        print("2. Sort Playlist")
        print("3. Display Playlist")
        print("4. Compare Sorting Algorithms")
        print("5. Save Playlist")
        print("6. Load Playlist")
        print("7. Generate Sample Playlist")
        print("8. View Sort History")
        print("9. Exit")

        choice = input("\nEnter your choice (1-9): ")

        try:
            if choice == "1":
                title = input("Enter track title: ")
                artist = input("Enter artist name: ")
                album = input("Enter album name: ")
                duration = int(input("Enter duration (seconds): "))
                genre = input("Enter genre: ")
                year = int(input("Enter year: "))
                plays = int(input("Enter number of plays: "))
                rating = float(input("Enter rating (0-5): "))

                track = Track(
                    title, artist, album, duration, genre, year, plays, rating
                )
                manager.add_track(track)
                print("Track added successfully!")

            elif choice == "2":
                if not manager.playlist:
                    print("Playlist is empty!")
                    continue

                print("\nSort by:")
                print("1. Title")
                print("2. Artist")
                print("3. Album")
                print("4. Duration")
                print("5. Genre")
                print("6. Year")
                print("7. Plays")
                print("8. Rating")

                sort_choice = input("Enter choice (1-8): ")
                sort_criteria = {
                    "1": "title",
                    "2": "artist",
                    "3": "album",
                    "4": "duration",
                    "5": "genre",
                    "6": "year",
                    "7": "plays",
                    "8": "rating",
                }.get(sort_choice, "title")

                print("\nSelect algorithm:")
                print("1. Quick Sort")
                print("2. Merge Sort")
                print("3. Bubble Sort")

                algo_choice = input("Enter choice (1-3): ")
                algorithm = {"1": "quick", "2": "merge", "3": "bubble"}.get(
                    algo_choice, "quick"
                )

                reverse = input("Sort in reverse order? (y/n): ").lower() == "y"

                sorted_playlist = manager.sort_playlist(
                    sort_criteria, algorithm, reverse
                )
                print("\nSorted Playlist:")
                for track in sorted_playlist:
                    print(f"\nTitle: {track.title}")
                    print(f"Artist: {track.artist}")
                    print(f"Duration: {track.format_duration()}")
                    print(f"Rating: {track.rating}")

            elif choice == "3":
                if not manager.playlist:
                    print("Playlist is empty!")
                    continue

                print("\nCurrent Playlist:")
                for i, track in enumerate(manager.playlist, 1):
                    print(f"\n{i}. {track.title} by {track.artist}")
                    print(f"   Album: {track.album}")
                    print(f"   Duration: {track.format_duration()}")
                    print(f"   Genre: {track.genre}")
                    print(f"   Year: {track.year}")
                    print(f"   Plays: {track.plays}")
                    print(f"   Rating: {track.rating}")

            elif choice == "4":
                if len(manager.playlist) < 2:
                    print("Need at least 2 tracks for comparison!")
                    continue

                performance = manager.get_sorting_performance()
                print("\nSorting Algorithm Performance:")
                for algorithm, time_taken in performance.items():
                    print(f"{algorithm.capitalize()} Sort: {time_taken:.6f} seconds")

            elif choice == "5":
                if not manager.playlist:
                    print("Playlist is empty!")
                    continue

                filename = input("Enter filename to save: ")
                manager.save_playlist(filename)
                print(f"Playlist saved to {filename}")

            elif choice == "6":
                filename = input("Enter filename to load: ")
                manager.load_playlist(filename)
                print("Playlist loaded successfully!")

            elif choice == "7":
                size = int(input("Enter number of tracks to generate: "))
                manager.playlist = generate_sample_playlist(size)
                print(f"Generated playlist with {size} tracks!")

            elif choice == "8":
                if not manager.sort_history:
                    print("No sort history available!")
                    continue

                print("\nSort History:")
                for i, entry in enumerate(manager.sort_history, 1):
                    print(f"\n{i}. Algorithm: {entry['algorithm']}")
                    print(f"   Criteria: {entry['criteria']}")
                    print(f"   Reverse: {entry['reverse']}")
                    print(f"   Time: {entry['execution_time']:.6f} seconds")
                    print(f"   Playlist Size: {entry['playlist_size']}")
                    print(f"   Timestamp: {entry['timestamp']}")

            elif choice == "9":
                print("Thank you for using the Music Playlist Sorter!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
