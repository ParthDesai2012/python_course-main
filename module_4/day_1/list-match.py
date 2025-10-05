list1 = [4, 5, 1, 2, 9, 7, 100, 8, 1]
print("Original List:", list1)
key = int(input("Enter a key:-"))
count = 0
for item in list1:
    if key == item:
        count += 1
if count == 0:
    print(f"The provided key {key} is missing!")
else:
    print(f"{key} has appeared {count} times in the list!")