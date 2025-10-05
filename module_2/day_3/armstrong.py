num = int(input("Enter a number: "))
original = num
n = len(str(num))
result = 0

while num > 0:
    digit = num % 10
    result += digit ** n
    num //= 10

if result == original:
    print("Armstrong number")
else:
    print("Not an Armstrong number")
