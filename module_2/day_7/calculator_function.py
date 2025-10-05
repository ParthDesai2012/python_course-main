def add(num1, num2):
    return num1 + num2
def subtract(num1, num2):
    return num1 - num2
def multiply(num1, num2):
    return num1 * num2
def divide(num1, num2):
    return num1 / num2
def exponentiate(num1, num2):
    return num1 ** num2
def floor_divide(num1, num2):
    return num1 // num2
def modulus(num1, num2):
    return num1 % num2

num1 = float(input("Enter the first number- "))
num2 = float(input("Enter the second number- "))
operator = input("Enter the operator- ")

if operator == "+":
    print(f"Result = {add(num1, num2)}")
elif operator == "-":
    print(f"Result = {subtract(num1, num2)}")
elif operator == "*":
    print(f"Result = {multiply(num1, num2)}")
elif operator == "/":     
    print(f"Result = {divide(num1, num2)}")
elif operator == "**":     
    print(f"Result = {exponentiate(num1, num2)}")
elif operator == "//":     
    print(f"Result = {floor_divide(num1, num2)}")
elif operator == "%":     
    print(f"Result = {modulus(num1, num2)}")
else:
    print("please enter a valid operator!")
    