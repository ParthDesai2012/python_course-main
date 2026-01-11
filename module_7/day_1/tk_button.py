import tkinter as tk
def on_click():
    entered_text = entry.get()
    label.config(text=f"Hello {entered_text}!")

root = tk.Tk()
root.title("Button Example")
root.geometry("600x300")

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Click Me", command=on_click)
button.pack()

label = tk.Label(root, text="Enter your name.")
label.pack()

root.mainloop()
