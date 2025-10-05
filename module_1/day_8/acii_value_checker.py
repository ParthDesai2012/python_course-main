# Get a character from the user
charecter = input("Enter a single character: ")
if len(charecter) == 1:
    ascii_value = ord(charecter)
    print(f"The ASCII value of '{charecter}' is {ascii_value}")
else:
    print("Please enter only one character.")
