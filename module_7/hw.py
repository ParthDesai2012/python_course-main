import tkinter as tk
def on_click():
    num1 = int(entry.get())
    num2 = int(entry2.get())
    ans = num1*num2
    label3.config(text=f"The product is {ans}")

root = tk.Tk()
root.title("Button Example")
root.geometry("600x300")

label = tk.Label(root, text="Enter the 1st number")
label.pack()
entry = tk.Entry(root)
entry.pack()

label2 = tk.Label(root, text="Enter the 2nd number")
label2.pack()
entry2 = tk.Entry(root)
entry2.pack()

label3 =  tk.Label(root, text="")
label3.pack()

button = tk.Button(root, text="=", command=on_click)
button.pack()



root.mainloop()
