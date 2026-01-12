#Write a Python Tkinter program that creates a 300x200 window titled "Security Trap". Bind events to the window so that left-clicking the mouse anywhere displays a warning pop-up saying "Intruder Detected", while pressing the Enter key displays an info pop-up saying "Access Granted".


from tkinter import *
from tkinter import messagebox

# Create window
root = Tk()
root.title("Security Trap")
root.geometry("300x200")

# Function for mouse click
def intruder(event):
    messagebox.showwarning("Warning", "Intruder Detected")

# Function for Enter key
def access(event):
    messagebox.showinfo("Info", "Access Granted")

# Bind events
root.bind("<Button-1>", intruder)   # Left mouse click
root.bind("<Button-2>", access)       # Enter key

# Run the application
root.mainloop()
