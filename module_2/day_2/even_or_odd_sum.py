num = int(input("Enter a number:- "))
command = input("Even Sum or Odd Sum?:- ")
even_sum = 0
odd_sum = 0
if command == "Even Sum":
    for i in range(0, num+1, 2):
        print(i)
        even_sum += i
    print(f"Even Sum = {even_sum}")
elif command == "Odd Sum":
    for i in range(1, num+1, 2):
        print(i)
        odd_sum += i
    print(f"Odd Sum = {odd_sum}")
