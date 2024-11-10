import os
from typing import List, Dict, Set, Optional, Generator, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import time


@dataclass
class FileStats:
    """Statistics for a file or directory."""

    size: int
    modified_time: datetime
    created_time: datetime
    is_directory: bool
    extension: Optional[str] = None


class DirectoryTreeGenerator:
    def __init__(self):
        self.ignored_dirs: Set[str] = {".git", "__pycache__", "node_modules", "venv"}
        self.ignored_files: Set[str] = {".DS_Store", "Thumbs.db"}
        self.ignored_extensions: Set[str] = {".pyc", ".pyo"}
        self.max_depth: Optional[int] = None
        self.statistics: Dict[str, int] = {
            "total_dirs": 0,
            "total_files": 0,
            "total_size": 0,
        }

    def reset_statistics(self) -> None:
        """Reset the statistics counters."""
        self.statistics = {"total_dirs": 0, "total_files": 0, "total_size": 0}

    def get_file_stats(self, path: str) -> FileStats:
        """Get statistics for a file or directory."""
        stats = os.stat(path)
        is_dir = os.path.isdir(path)
        extension = os.path.splitext(path)[1] if not is_dir else None

        return FileStats(
            size=stats.st_size,
            modified_time=datetime.fromtimestamp(stats.st_mtime),
            created_time=datetime.fromtimestamp(stats.st_ctime),
            is_directory=is_dir,
            extension=extension,
        )

    def should_ignore(self, name: str, is_dir: bool) -> bool:
        """Check if a file or directory should be ignored."""
        if is_dir and name in self.ignored_dirs:
            return True
        if not is_dir:
            if name in self.ignored_files:
                return True
            if os.path.splitext(name)[1] in self.ignored_extensions:
                return True
        return False

    def generate_tree(
        self, root_path: str, depth: int = 0
    ) -> Generator[Tuple[int, str, FileStats], None, None]:
        """Generate directory tree structure recursively."""
        if self.max_depth is not None and depth > self.max_depth:
            return

        try:
            # Get list of items in directory
            items = os.listdir(root_path)
            items.sort()  # Sort alphabetically

            for item in items:
                full_path = os.path.join(root_path, item)
                is_dir = os.path.isdir(full_path)

                # Check if item should be ignored
                if self.should_ignore(item, is_dir):
                    continue

                # Get file/directory statistics
                stats = self.get_file_stats(full_path)

                # Update statistics
                if is_dir:
                    self.statistics["total_dirs"] += 1
                else:
                    self.statistics["total_files"] += 1
                    self.statistics["total_size"] += stats.size

                # Yield current item
                yield depth, item, stats

                # Recursively process directories
                if is_dir:
                    yield from self.generate_tree(full_path, depth + 1)

        except (PermissionError, FileNotFoundError) as e:
            print(f"Error accessing {root_path}: {str(e)}")

    def print_tree(self, root_path: str) -> None:
        """Print directory tree structure."""
        self.reset_statistics()
        start_time = time.time()

        print(f"\nDirectory Tree for: {root_path}")
        print("=" * 50)

        for depth, name, stats in self.generate_tree(root_path):
            # Create indent based on depth
            indent = "│   " * (depth) + "├── "

            # Format size
            size_str = self.format_size(stats.size) if not stats.is_directory else "DIR"

            # Format last modified time
            modified_time_str = stats.modified_time.strftime("%Y-%m-%d %H:%M:%S")

            print(f"{indent}{name} ({size_str}, Modified: {modified_time_str})")

        duration = time.time() - start_time
        self.print_statistics(duration)

    def format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    def print_statistics(self, duration: float) -> None:
        """Print directory statistics."""
        print("\nDirectory Statistics:")
        print("=" * 50)
        print(f"Total Directories: {self.statistics['total_dirs']}")
        print(f"Total Files: {self.statistics['total_files']}")
        print(f"Total Size: {self.format_size(self.statistics['total_size'])}")
        print(f"Scan Duration: {duration:.2f} seconds")

    def find_largest_files(self, root_path: str, n: int = 10) -> List[Tuple[str, int]]:
        """Find the n largest files in the directory tree."""
        large_files: List[Tuple[str, int]] = []

        def traverse(path: str) -> None:
            try:
                for item in os.listdir(path):
                    full_path = os.path.join(path, item)
                    if os.path.isfile(full_path) and not self.should_ignore(
                        item, False
                    ):
                        size = os.path.getsize(full_path)
                        large_files.append((full_path, size))
                        large_files.sort(key=lambda x: x[1], reverse=True)
                        if len(large_files) > n:
                            large_files.pop()
                    elif os.path.isdir(full_path) and not self.should_ignore(
                        item, True
                    ):
                        traverse(full_path)
            except (PermissionError, FileNotFoundError):
                pass

        traverse(root_path)
        return large_files

    def find_duplicate_files(self, root_path: str) -> Dict[int, List[str]]:
        """Find duplicate files based on size."""
        size_map: Dict[int, List[str]] = {}

        def traverse(path: str) -> None:
            try:
                for item in os.listdir(path):
                    full_path = os.path.join(path, item)
                    if os.path.isfile(full_path) and not self.should_ignore(
                        item, False
                    ):
                        size = os.path.getsize(full_path)
                        if size in size_map:
                            size_map[size].append(full_path)
                        else:
                            size_map[size] = [full_path]
                    elif os.path.isdir(full_path) and not self.should_ignore(
                        item, True
                    ):
                        traverse(full_path)
            except (PermissionError, FileNotFoundError):
                pass

        traverse(root_path)
        return {size: paths for size, paths in size_map.items() if len(paths) > 1}

    def save_tree(self, root_path: str, output_file: str) -> None:
        """Save directory tree structure to a file."""
        self.reset_statistics()

        def create_tree_dict(path: str) -> Dict:
            tree = {"name": os.path.basename(path) or path}
            try:
                if os.path.isdir(path):
                    stats = self.get_file_stats(path)
                    tree.update(
                        {
                            "type": "directory",
                            "stats": {
                                "size": stats.size,
                                "modified_time": stats.modified_time.isoformat(),
                                "created_time": stats.created_time.isoformat(),
                            },
                            "children": [],
                        }
                    )

                    for item in sorted(os.listdir(path)):
                        full_path = os.path.join(path, item)
                        if not self.should_ignore(item, os.path.isdir(full_path)):
                            tree["children"].append(create_tree_dict(full_path))
                else:
                    stats = self.get_file_stats(path)
                    tree.update(
                        {
                            "type": "file",
                            "stats": {
                                "size": stats.size,
                                "modified_time": stats.modified_time.isoformat(),
                                "created_time": stats.created_time.isoformat(),
                                "extension": stats.extension,
                            },
                        }
                    )
            except (PermissionError, FileNotFoundError) as e:
                tree["error"] = str(e)

            return tree

        tree_data = create_tree_dict(root_path)
        with open(output_file, "w") as f:
            json.dump(tree_data, f, indent=4)


def main():
    generator = DirectoryTreeGenerator()

    while True:
        print("\nDirectory Tree Generator")
        print("1. Generate Tree")
        print("2. Find Largest Files")
        print("3. Find Duplicate Files")
        print("4. Save Tree to File")
        print("5. Configure Ignored Items")
        print("6. Set Maximum Depth")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        try:
            if choice == "1":
                path = input("Enter directory path: ")
                if os.path.exists(path):
                    generator.print_tree(path)
                else:
                    print("Directory does not exist!")

            elif choice == "2":
                path = input("Enter directory path: ")
                n = int(input("How many largest files to find? "))
                if os.path.exists(path):
                    large_files = generator.find_largest_files(path, n)
                    print("\nLargest Files:")
                    for file_path, size in large_files:
                        print(f"{file_path}: {generator.format_size(size)}")
                else:
                    print("Directory does not exist!")

            elif choice == "3":
                path = input("Enter directory path: ")
                if os.path.exists(path):
                    duplicates = generator.find_duplicate_files(path)
                    if duplicates:
                        print("\nPotential Duplicate Files (based on size):")
                        for size, files in duplicates.items():
                            print(f"\nSize: {generator.format_size(size)}")
                            for file in files:
                                print(f"  {file}")
                    else:
                        print("No duplicate files found.")
                else:
                    print("Directory does not exist!")

            elif choice == "4":
                path = input("Enter directory path: ")
                output_file = input("Enter output file path: ")
                if os.path.exists(path):
                    generator.save_tree(path, output_file)
                    print(f"Tree structure saved to {output_file}")
                else:
                    print("Directory does not exist!")

            elif choice == "5":
                print("\nConfigure Ignored Items:")
                print("1. Add ignored directory")
                print("2. Add ignored file")
                print("3. Add ignored extension")
                print("4. View ignored items")
                print("5. Clear ignored items")

                config_choice = input("Enter choice (1-5): ")

                if config_choice == "1":
                    dir_name = input("Enter directory name to ignore: ")
                    generator.ignored_dirs.add(dir_name)
                elif config_choice == "2":
                    file_name = input("Enter file name to ignore: ")
                    generator.ignored_files.add(file_name)
                elif config_choice == "3":
                    ext = input("Enter extension to ignore (with dot): ")
                    generator.ignored_extensions.add(ext)
                elif config_choice == "4":
                    print("\nIgnored Directories:", generator.ignored_dirs)
                    print("Ignored Files:", generator.ignored_files)
                    print("Ignored Extensions:", generator.ignored_extensions)
                elif config_choice == "5":
                    generator.ignored_dirs = set()
                    generator.ignored_files = set()
                    generator.ignored_extensions = set()
                    print("All ignored items cleared.")

            elif choice == "6":
                depth = input("Enter maximum depth (empty for unlimited): ")
                generator.max_depth = int(depth) if depth else None
                print(f"Maximum depth set to: {depth if depth else 'unlimited'}")

            elif choice == "7":
                print("Thank you for using Directory Tree Generator!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
