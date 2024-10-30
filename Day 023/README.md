# Day 23 Sets and frozen sets - Mini Project: Duplicate File Finder

![File Finder](/Day%20023/file.png)


## Duplicate File Finder

This project will help you understand how to use sets for efficient comparison and deduplication operations.

### Key Concepts

Let's break down the key concepts of Sets and Frozen Sets used in this Duplicate File Finder:

#### Set Operations
```python
# Set creation
self.scanned_paths: Set[Path] = set()

# Adding to sets
self.scanned_paths.add(directory)

# Set methods
self.ignored_extensions.discard(extension.lower())
```

#### Frozen Sets
```python
# Create immutable sets of duplicate files
duplicates[frozenset(file_set)] = len(file_set)
```

#### Set Comprehension
```python
# Union of all file sets
set.union(*[set(files) for files in self.file_hashes.values()])
```

#### DefaultDict with Sets
```python
self.file_hashes: Dict[str, Set[Path]] = defaultdict(set)
```

#### Set Theory Operations
```python
# Finding duplicates using set properties
if len(file_set) > 1:  # Set cardinality
```

### Key Features

#### File Analysis
- Content-based comparison
- Name-based comparison
- Size-based comparison

#### Duplicate Management
- Find duplicates
- Move duplicates
- Generate reports

#### Extension Filtering
- Ignore specific extensions
- Manage ignored extensions

#### Statistics
- Total files
- Duplicate groups
- Wasted space