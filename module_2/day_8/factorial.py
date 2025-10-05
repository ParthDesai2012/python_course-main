x = int(input("Enter a number:-"))
def factorial(x):
    if x == 0 or x == 1:
        return 1
    else:  
        return x*factorial(x-1)
print(f"factorial of {x} is {factorial(x)}")