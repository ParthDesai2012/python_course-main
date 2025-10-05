number = int(input("Enter a number: "))
binary = ""
while number > 0:
    remainder = number % 2
    binary = str(remainder) + binary
    number = number // 2
print(f"Binary number is:", binary)
