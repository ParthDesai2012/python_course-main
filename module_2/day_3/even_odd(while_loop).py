num = int(input("Enter a number:- "))
command = input("Even Sum or Odd Sum?:- ")
even_sum = 0
odd_sum = 0
if command == "Even Sum":
    i = 0
    while i < num+1:
        print(i)
        even_sum += i
        i += 2
    print(f"Even Sum = {even_sum}")
elif command == "Odd Sum":
    i = 1
    while i < num+1:
        print(i)
        odd_sum += i
        i += 2
    print(f"Odd Sum = {odd_sum}")