num = int(input("Enter a number:-"))
for i in range (100):
    if i == num :
        break
    if i % 2 == 0:
        continue
    if i % 3 == 0:
        print("Fizz")
    if i % 5 == 0:
        print("Buzz")
    print(i)