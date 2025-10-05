num = input("Enter a number: ")
count = 0
for i in range(len(num)):
    if num[i].isdigit():
        count += 1
print("Total number of digits:", count)
