n = int(input("Enter a number: "))
odd_numbers = [i for i in range(1, n) if i % 2 != 0]
even_numbers = [i for i in range(1, n) if i % 2 == 0]
print("\nOdd numbers:", odd_numbers)
print("Even numbers:", even_numbers)
fruits = ['apple', 'banana', 'cherry', 'mango', 'grape']
updated_fruits = [fruit.capitalize() for fruit in fruits]
print("Original fruits list:", fruits)
print("Updated fruits list:", updated_fruits)
