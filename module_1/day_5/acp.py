# take buying and selling price from the user
# find out if it is a profit or loss and print the value
bp = int(input("Enter the buying price: "))
sp = int(input("Enter the selling price: "))
if sp > bp:
    p = sp - bp
    print(f"Profit: {p}")
else:
    l = bp - sp
    print(f"Loss: {l}")
