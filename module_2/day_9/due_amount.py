paid = int(input("Enter the amount paid :- "))
bill = int(input("Enter the amount needed to pay:- "))
def due(paid, bill):
    return bill - paid
def change(paid, bill):
    return paid - bill
if paid < bill:
    print(f"Due amount is {due(paid, bill)}")
elif paid == bill: 
    print("no value is due")
else:
    print(f"The cashier needs to give {change(paid, bill)}")