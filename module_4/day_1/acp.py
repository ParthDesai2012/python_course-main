start = int(input("Enter the starting number: "))
end = int(input("Enter the ending number: "))
squares = [x**2 for x in range(start, end + 1)]
print("Squares of numbers:", squares)
even_squares = [num for num in squares if num % 2 == 0]
odd_squares = [num for num in squares if num % 2 != 0]
print("Even squares:", even_squares)
print("Odd squares:", odd_squares)