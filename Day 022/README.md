# Day 22 Advanced dictionary operations - Mini Project: Word Frequency Counter

![Word Counter](/Day%20022/word.png)

# Word Frequency Counter

This project showcases dictionary comprehensions, nested dictionaries, and various dictionary manipulation techniques.

Let's break down the advanced dictionary operations used in this Word Frequency Counter:

### Dictionary Comprehension:
```python
# Create frequency dictionary
word_counts = Counter(word for word in words 
                     if not (ignore_stop_words and word in self.stop_words))
```

### Counter Class:
```python
# Combine frequency dictionaries
self.word_frequencies = dict(Counter(self.word_frequencies) + word_counts)
```

### Dictionary Methods:
```python
# Get method with default value
self.word_frequencies.get(word, 0)
```

### Dictionary Merging:
```python
# Merge statistics into analysis dictionary
analysis = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'statistics': self.get_statistics(),
    'word_frequencies': self.word_frequencies,
    # ...
}
```

### Dictionary Operations in Comprehensions:
```python
# Calculate average word length
sum(len(word) * freq for word, freq in self.word_frequencies.items())
```

### Nested Dictionaries:
```python
# Statistics dictionary with nested values
return {
    'total_words': self.total_words,
    'unique_words': self.unique_words,
    'average_word_length': average_length,
    # ...
}
```

## Key Features:

### Text Analysis:
- Word frequency counting
- Case-sensitive/insensitive options
- Stop word filtering

### Statistics:
- Total word count
- Unique word count
- Average word length
- Lexical diversity

### Visualization:
- ASCII word cloud generation
- Frequency distribution

### Data Management:
- Save/Load analysis results
- File processing support
