num = int(input("Enter a number:- "))
is_prime = True
if num >= 2:
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
           is_prime = False
if is_prime:
    print(f"{num} is a prime number")
else:
    print(f"{num} is not a prime number")
