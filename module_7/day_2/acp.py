import tkinter as tk
from tkinter import messagebox
from datetime import date

# Function to calculate age
def calculate_age():
    try:
        day = int(day_entry.get())
        month = int(month_entry.get())
        year = int(year_entry.get())

        birth_date = date(year, month, day)
        today = date.today()

        # Age calculation
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        result_label.config(text=f"Your present age is: {age} years")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for date, month, and year.")

# Create window
root = tk.Tk()
root.title("Age Calculator")
root.geometry("300x250")

# Labels and Entry fields
tk.Label(root, text="Enter Date of Birth", font=("Arial", 14)).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Day").grid(row=0, column=0, padx=5)
day_entry = tk.Entry(frame, width=5)
day_entry.grid(row=0, column=1)

tk.Label(frame, text="Month").grid(row=1, column=0, padx=5)
month_entry = tk.Entry(frame, width=5)
month_entry.grid(row=1, column=1)

tk.Label(frame, text="Year").grid(row=2, column=0, padx=5)
year_entry = tk.Entry(frame, width=5)
year_entry.grid(row=2, column=1)

# Button
tk.Button(root, text="Calculate Age", command=calculate_age).pack(pady=10)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

# Run app
root.mainloop()
