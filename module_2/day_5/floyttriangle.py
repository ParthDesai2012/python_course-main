row = int(input("Enter rows:- "))
num = 1
for i in range(row):
    for j in range(i+1):
        print(num, end=" ")
        num += 1
    print()