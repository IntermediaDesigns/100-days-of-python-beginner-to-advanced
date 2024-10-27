# Day 19 Date and time operations - Mini Project: Countdown Timer and Stopwatch

![Timer](/Day%20019/timer.mp4)

## Countdown Timer and Stopwatch

This project will help you understand how to work with time intervals, formatting, and real-time updates.

### Key Concepts of Date and Time Operations

#### Time Measurement

```python
time.time()  # Get current time in seconds since epoch
```

#### Time Formatting

```python
def format_time(self, seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
```

#### Time Calculations

```python
elapsed_time = time.time() - start_time
remaining_time = target_time - elapsed_time
```

#### Threading for Real-time Updates

```python
self.display_thread = threading.Thread(target=self.display_timer)
self.display_thread.start()
```

#### Time Delays

```python
time.sleep(0.1)  # Pause execution for 0.1 seconds
```

#### Time Duration Management

```python
def set_duration(self, hours, minutes, seconds):
    total_seconds = hours * 3600 + minutes * 60 + seconds
```

### Important Concepts Demonstrated

#### Object-Oriented Programming

- Base Timer class with common functionality
- CountdownTimer class inheriting from Timer
- TimerApplication class managing the application

#### Real-time Updates

- Threading for continuous display updates
- Keyboard input handling

#### Time Management

- Converting between different time units
- Tracking elapsed and remaining time
- Handling pauses and resumptions

## How to Run This Project

1. **Install the required package:**

   ```bash
   pip install keyboard
   ```

2. **Copy the code into a new Python file (e.g., `timer_app.py`).**

3. **Run the file using Python:**

   ```bash
   python timer_app.py
   ```

4. **Follow the prompts to use either the stopwatch or countdown timer.**
