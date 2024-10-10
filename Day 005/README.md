# Day 5: RGB Color Mixer Application

![Color Mixer](/Day%20005/color.png)

## Key Concepts Related to Tuples and Named Tuples

### Regular Tuples
- While not explicitly used in the final code, regular tuples could be used to represent RGB colors, e.g., `(255, 0, 0)` for red.
- Tuples are immutable, making them suitable for representing fixed color values.

### Named Tuples
- We use `namedtuple` from the `collections` module to create a `Color` class:
  ```python
  from collections import namedtuple
  Color = namedtuple('Color', ['red', 'green', 'blue'])
  ```
- This creates a tuple-like object with named fields, improving readability and self-documentation.

### Creating Named Tuples
- We create `Color` objects using the `create_color` function:
  ```python
  def create_color(red, green, blue):
      return Color(
          max(0, min(255, red)),
          max(0, min(255, green)),
          max(0, min(255, blue))
      )
  ```
- This ensures that color values are within the valid range (0-255).

### Accessing Named Tuple Fields
- We can access color components using dot notation, e.g., `color.red`, `color.green`, `color.blue`.
- This is more readable than index-based access used with regular tuples.

### Immutability
- Like regular tuples, named tuples are immutable. We create new `Color` objects rather than modifying existing ones (e.g., in the `mix_colors` function).

### Tuple Unpacking
- While not explicitly used here, tuple unpacking can be useful with named tuples:
  ```python
  r, g, b = some_color  # Unpacks into individual variables
  ```

### Converting to Other Types
- We convert `Color` objects to hex strings in the `color_to_hex` function, demonstrating how to work with the tuple data.

## To Run This Project
1. Copy the code into a new Python file (e.g., `rgb_color_mixer.py`).
2. Run the file using Python (e.g., `python rgb_color_mixer.py` in the command line).
3. Follow the prompts to create custom colors, mix colors, or generate random colors.