num = int(input("Enter a number:- "))
power = int(input("Enter the power of the number:- "))
result = 1
for i in range(power):
    result *= num
print(result)