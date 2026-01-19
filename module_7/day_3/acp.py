import tkinter as tk

def convert():
    try:
        inches = float(entry.get())
        cm = inches * 2.54
        result_label.config(text=f"{cm:.2f} cm")
    except ValueError:
        result_label.config(text="Enter a valid number!")

root = tk.Tk()
root.title("Inches to Centimeters Converter")
root.geometry("300x200")

title = tk.Label(root, text="Inches → Centimeters", font=("Arial", 14))
title.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

btn = tk.Button(root, text="Convert", command=convert)
btn.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
