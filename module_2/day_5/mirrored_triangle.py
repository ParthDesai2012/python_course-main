rows = int(input("Enter the number of rows: "))
for i in range(1, rows + 1):
    spaces = ' ' * (2 * (rows - i))
    stars = '* ' * i
    print(spaces + stars)