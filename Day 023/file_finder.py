import os
import hashlib
from pathlib import Path
from typing import Dict, Set, FrozenSet, List, Generator, Tuple
from collections import defaultdict
import json
from datetime import datetime
import shutil


class DuplicateFileFinder:
    def __init__(self):
        self.file_hashes: Dict[str, Set[Path]] = defaultdict(set)
        self.size_groups: Dict[int, Set[Path]] = defaultdict(set)
        self.name_groups: Dict[str, Set[Path]] = defaultdict(set)
        self.scanned_paths: Set[Path] = set()
        self.ignored_extensions: Set[str] = set()
        self.scan_history: List[Dict] = []

    def calculate_file_hash(self, file_path: Path, chunk_size: int = 8192) -> str:
        """Calculate MD5 hash of a file."""
        hasher = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (PermissionError, FileNotFoundError):
            return ""

    def scan_directory(self, directory: Path) -> None:
        """Scan directory for files and organize them by hash, size, and name."""
        try:
            # Convert to Path object if string is provided
            directory = Path(directory)

            # Add to scanned paths
            self.scanned_paths.add(directory)

            # Scan all files in directory and subdirectories
            for file_path in self._scan_files(directory):
                # Skip files with ignored extensions
                if file_path.suffix.lower() in self.ignored_extensions:
                    continue

                # Group by size
                size = file_path.stat().st_size
                self.size_groups[size].add(file_path)

                # Group by name
                name = file_path.name
                self.name_groups[name].add(file_path)

                # Calculate hash only for files in same-size groups
                if len(self.size_groups[size]) > 1:
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash:
                        self.file_hashes[file_hash].add(file_path)

            # Record scan in history
            self.scan_history.append(
                {
                    "directory": str(directory),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "files_scanned": sum(
                        len(files) for files in self.file_hashes.values()
                    ),
                }
            )

        except Exception as e:
            raise Exception(f"Error scanning directory: {str(e)}")

    def _scan_files(self, directory: Path) -> Generator[Path, None, None]:
        """Generator to yield all files in directory and subdirectories."""
        try:
            for item in directory.rglob("*"):
                if item.is_file():
                    yield item
        except PermissionError:
            pass

    def get_duplicate_files(
        self, method: str = "content"
    ) -> Dict[FrozenSet[Path], int]:
        """Get duplicate files grouped by their duplicate criterion."""
        duplicates: Dict[FrozenSet[Path], int] = {}

        if method == "content":
            source_dict = self.file_hashes
        elif method == "size":
            source_dict = self.size_groups
        elif method == "name":
            source_dict = self.name_groups
        else:
            raise ValueError("Invalid method. Use 'content', 'size', or 'name'")

        # Use set operations to find duplicates
        for key, file_set in source_dict.items():
            if len(file_set) > 1:
                duplicates[frozenset(file_set)] = len(file_set)

        return duplicates

    def add_ignored_extension(self, extension: str) -> None:
        """Add file extension to ignore list."""
        if not extension.startswith("."):
            extension = f".{extension}"
        self.ignored_extensions.add(extension.lower())

    def remove_ignored_extension(self, extension: str) -> None:
        """Remove file extension from ignore list."""
        if not extension.startswith("."):
            extension = f".{extension}"
        self.ignored_extensions.discard(extension.lower())

    def get_statistics(self) -> Dict:
        """Get statistics about scanned files and duplicates."""
        duplicate_sets = self.get_duplicate_files("content")
        total_duplicates = sum(
            len(duplicate_set) - 1 for duplicate_set in duplicate_sets.keys()
        )
        wasted_space = sum(
            next(iter(duplicate_set)).stat().st_size * (len(duplicate_set) - 1)
            for duplicate_set in duplicate_sets.keys()
        )

        return {
            "total_files_scanned": sum(
                len(files) for files in self.file_hashes.values()
            ),
            "unique_files": (
                len(set.union(*[set(files) for files in self.file_hashes.values()]))
                if self.file_hashes
                else 0
            ),
            "duplicate_groups": len(duplicate_sets),
            "total_duplicates": total_duplicates,
            "wasted_space_bytes": wasted_space,
            "scanned_directories": len(self.scanned_paths),
        }

    def save_report(self, filename: str) -> None:
        """Save duplicate analysis report to file."""
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "statistics": self.get_statistics(),
            "duplicates": {
                "by_content": {
                    str(k): [str(p) for p in v]
                    for k, v in self.get_duplicate_files("content").items()
                },
                "by_name": {
                    str(k): [str(p) for p in v]
                    for k, v in self.get_duplicate_files("name").items()
                },
            },
            "scan_history": self.scan_history,
        }

        with open(filename, "w") as f:
            json.dump(report, f, indent=4)

    def move_duplicates(self, destination: Path, group_id: str) -> None:
        """Move duplicate files to a specified directory."""
        try:
            destination = Path(destination)
            destination.mkdir(parents=True, exist_ok=True)

            # Get the duplicate group
            duplicates = self.get_duplicate_files("content")
            for duplicate_set in duplicates.keys():
                if hashlib.md5(str(duplicate_set).encode()).hexdigest()[:8] == group_id:
                    # Keep the first file, move the rest
                    duplicate_list = list(duplicate_set)
                    for file_path in duplicate_list[1:]:
                        new_path = destination / file_path.name
                        # Ensure unique filename
                        if new_path.exists():
                            base = new_path.stem
                            suffix = new_path.suffix
                            counter = 1
                            while new_path.exists():
                                new_path = destination / f"{base}_{counter}{suffix}"
                                counter += 1
                        shutil.move(str(file_path), str(new_path))
                    break
        except Exception as e:
            raise Exception(f"Error moving duplicates: {str(e)}")


def format_size(size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def main():
    finder = DuplicateFileFinder()

    while True:
        print("\nDuplicate File Finder")
        print("1. Scan Directory")
        print("2. Show Duplicate Files")
        print("3. Show Statistics")
        print("4. Manage Ignored Extensions")
        print("5. Generate Report")
        print("6. Move Duplicates")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        try:
            if choice == "1":
                directory = input("Enter directory path to scan: ")
                finder.scan_directory(Path(directory))
                print("Scan completed successfully!")

            elif choice == "2":
                print("\nSelect duplicate search method:")
                print("1. By Content")
                print("2. By Name")
                print("3. By Size")

                method_choice = input("Enter choice (1-3): ")
                method = {"1": "content", "2": "name", "3": "size"}.get(method_choice)

                if method:
                    duplicates = finder.get_duplicate_files(method)
                    if duplicates:
                        print(f"\nFound {len(duplicates)} groups of duplicates:")
                        for duplicate_set in duplicates:
                            print("\nDuplicate Group:")
                            group_id = hashlib.md5(
                                str(duplicate_set).encode()
                            ).hexdigest()[:8]
                            print(f"Group ID: {group_id}")
                            for file_path in duplicate_set:
                                size = format_size(file_path.stat().st_size)
                                print(f"- {file_path} ({size})")
                    else:
                        print("No duplicates found.")

            elif choice == "3":
                stats = finder.get_statistics()
                print("\nStatistics:")
                print(f"Total files scanned: {stats['total_files_scanned']}")
                print(f"Unique files: {stats['unique_files']}")
                print(f"Duplicate groups: {stats['duplicate_groups']}")
                print(f"Total duplicates: {stats['total_duplicates']}")
                print(f"Wasted space: {format_size(stats['wasted_space_bytes'])}")
                print(f"Scanned directories: {stats['scanned_directories']}")

            elif choice == "4":
                print("\n1. Add ignored extension")
                print("2. Remove ignored extension")
                print("3. Show ignored extensions")

                ext_choice = input("Enter choice (1-3): ")

                if ext_choice == "1":
                    ext = input("Enter extension to ignore (e.g., .tmp): ")
                    finder.add_ignored_extension(ext)
                    print(f"Added {ext} to ignored extensions.")
                elif ext_choice == "2":
                    ext = input("Enter extension to remove from ignore list: ")
                    finder.remove_ignored_extension(ext)
                    print(f"Removed {ext} from ignored extensions.")
                elif ext_choice == "3":
                    print("\nIgnored extensions:")
                    for ext in finder.ignored_extensions:
                        print(ext)

            elif choice == "5":
                filename = input("Enter report filename: ")
                finder.save_report(filename)
                print(f"Report saved to {filename}")

            elif choice == "6":
                group_id = input("Enter group ID of duplicates to move: ")
                dest_dir = input("Enter destination directory: ")
                finder.move_duplicates(Path(dest_dir), group_id)
                print("Duplicates moved successfully!")

            elif choice == "7":
                print("Thank you for using Duplicate File Finder!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
