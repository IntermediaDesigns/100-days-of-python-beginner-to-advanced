import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, timedelta


class TimerStopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer & Stopwatch")

        # Variables
        self.timer_running = False
        self.stopwatch_running = False
        self.timer_time = 0
        self.stopwatch_time = 0
        self.timer_after_id = None
        self.stopwatch_after_id = None

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Timer tab
        self.timer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.timer_frame, text="Timer")

        # Stopwatch tab
        self.stopwatch_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stopwatch_frame, text="Stopwatch")

        self.setup_timer()
        self.setup_stopwatch()

    def setup_timer(self):
        # Timer input frame
        input_frame = ttk.Frame(self.timer_frame)
        input_frame.pack(pady=10)

        # Time input fields
        ttk.Label(input_frame, text="Hours:").grid(row=0, column=0)
        self.hours_var = tk.StringVar(value="0")
        ttk.Entry(input_frame, textvariable=self.hours_var, width=5).grid(
            row=0, column=1
        )

        ttk.Label(input_frame, text="Minutes:").grid(row=0, column=2)
        self.minutes_var = tk.StringVar(value="0")
        ttk.Entry(input_frame, textvariable=self.minutes_var, width=5).grid(
            row=0, column=3
        )

        ttk.Label(input_frame, text="Seconds:").grid(row=0, column=4)
        self.seconds_var = tk.StringVar(value="0")
        ttk.Entry(input_frame, textvariable=self.seconds_var, width=5).grid(
            row=0, column=5
        )

        # Timer display
        self.timer_label = ttk.Label(
            self.timer_frame, text="00:00:00", font=("Arial", 30)
        )
        self.timer_label.pack(pady=20)

        # Timer buttons
        button_frame = ttk.Frame(self.timer_frame)
        button_frame.pack(pady=10)

        self.timer_start_button = ttk.Button(
            button_frame, text="Start", command=self.start_timer
        )
        self.timer_start_button.grid(row=0, column=0, padx=5)

        self.timer_pause_button = ttk.Button(
            button_frame, text="Pause", command=self.pause_timer, state="disabled"
        )
        self.timer_pause_button.grid(row=0, column=1, padx=5)

        self.timer_reset_button = ttk.Button(
            button_frame, text="Reset", command=self.reset_timer
        )
        self.timer_reset_button.grid(row=0, column=2, padx=5)

    def setup_stopwatch(self):
        # Stopwatch display
        self.stopwatch_label = ttk.Label(
            self.stopwatch_frame, text="00:00:00", font=("Arial", 30)
        )
        self.stopwatch_label.pack(pady=20)

        # Stopwatch buttons
        button_frame = ttk.Frame(self.stopwatch_frame)
        button_frame.pack(pady=10)

        self.stopwatch_start_button = ttk.Button(
            button_frame, text="Start", command=self.start_stopwatch
        )
        self.stopwatch_start_button.grid(row=0, column=0, padx=5)

        self.stopwatch_pause_button = ttk.Button(
            button_frame, text="Pause", command=self.pause_stopwatch, state="disabled"
        )
        self.stopwatch_pause_button.grid(row=0, column=1, padx=5)

        self.stopwatch_reset_button = ttk.Button(
            button_frame, text="Reset", command=self.reset_stopwatch
        )
        self.stopwatch_reset_button.grid(row=0, column=2, padx=5)

        # Lap time display
        self.lap_frame = ttk.Frame(self.stopwatch_frame)
        self.lap_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.lap_listbox = tk.Listbox(self.lap_frame, height=5)
        self.lap_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            self.lap_frame, orient=tk.VERTICAL, command=self.lap_listbox.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lap_listbox.config(yscrollcommand=scrollbar.set)

        self.lap_button = ttk.Button(
            self.stopwatch_frame, text="Lap", command=self.add_lap, state="disabled"
        )
        self.lap_button.pack(pady=5)

    def start_timer(self):
        if not self.timer_running:
            try:
                hours = int(self.hours_var.get())
                minutes = int(self.minutes_var.get())
                seconds = int(self.seconds_var.get())
                self.timer_time = hours * 3600 + minutes * 60 + seconds
                if self.timer_time > 0:
                    self.timer_running = True
                    self.timer_start_button.config(state="disabled")
                    self.timer_pause_button.config(state="normal")
                    self.update_timer()
            except ValueError:
                pass

    def update_timer(self):
        if self.timer_running and self.timer_time > 0:
            self.timer_time -= 1
            hours = self.timer_time // 3600
            minutes = (self.timer_time % 3600) // 60
            seconds = self.timer_time % 60
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.timer_after_id = self.root.after(1000, self.update_timer)
        elif self.timer_time <= 0:
            self.timer_label.config(text="Time's up!")
            self.timer_running = False
            self.timer_start_button.config(state="normal")
            self.timer_pause_button.config(state="disabled")

    def pause_timer(self):
        self.timer_running = False
        self.timer_start_button.config(state="normal")
        self.timer_pause_button.config(state="disabled")
        if self.timer_after_id:
            self.root.after_cancel(self.timer_after_id)

    def reset_timer(self):
        self.timer_running = False
        self.timer_time = 0
        self.timer_label.config(text="00:00:00")
        self.timer_start_button.config(state="normal")
        self.timer_pause_button.config(state="disabled")
        self.hours_var.set("0")
        self.minutes_var.set("0")
        self.seconds_var.set("0")
        if self.timer_after_id:
            self.root.after_cancel(self.timer_after_id)

    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.stopwatch_start_button.config(state="disabled")
            self.stopwatch_pause_button.config(state="normal")
            self.lap_button.config(state="normal")
            self.update_stopwatch()

    def update_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_time += 1
            hours = self.stopwatch_time // 3600
            minutes = (self.stopwatch_time % 3600) // 60
            seconds = self.stopwatch_time % 60
            self.stopwatch_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.stopwatch_after_id = self.root.after(1000, self.update_stopwatch)

    def pause_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_start_button.config(state="normal")
        self.stopwatch_pause_button.config(state="disabled")
        self.lap_button.config(state="disabled")
        if self.stopwatch_after_id:
            self.root.after_cancel(self.stopwatch_after_id)

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.stopwatch_label.config(text="00:00:00")
        self.stopwatch_start_button.config(state="normal")
        self.stopwatch_pause_button.config(state="disabled")
        self.lap_button.config(state="disabled")
        self.lap_listbox.delete(0, tk.END)
        if self.stopwatch_after_id:
            self.root.after_cancel(self.stopwatch_after_id)

    def add_lap(self):
        current_time = self.stopwatch_label.cget("text")
        lap_count = self.lap_listbox.size() + 1
        self.lap_listbox.insert(tk.END, f"Lap {lap_count}: {current_time}")
        self.lap_listbox.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerStopwatch(root)
    root.mainloop()
