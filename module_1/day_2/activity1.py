# import keyword
#print(keyword.kwlist)

chemistry = int(input("Enter your chemistry marks: "))  # str => int
physics = input("Enter your physics marks: ")  # "98"
biology = input("Enter your biology marks: ")
math = input("Enter your math marks: ")
average = (chemistry + physics + biology + math) / 4

print(f'chemistry = {chemistry}, physics = {physics}, biology = {biology}, math = {math}, average = {average}')

