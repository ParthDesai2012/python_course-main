try:
    age = int(input("Enter a valid age: "))
    if age <= 0 or age >= 78:  # Invalid age
        raise ValueError
    else:
        print("Age is valid!")
        if age % 2 == 0:
            print("The Age is Even!")
        else:
            print("The Age is Odd!")
except ValueError:
    print("Please enter a valid age!")
