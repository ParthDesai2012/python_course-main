key = input("Enter the key to search: ")
text = input("Enter the string: ")

count = 0
for i in range(len(text) - len(key) + 1):
    if text[i:i+len(key)] == key:
        count += 1

if count > 0:
    print(f"The key '{key}' appears {count} times in the string.")
else:
    print(f"The key '{key}' does not appear in the string.")