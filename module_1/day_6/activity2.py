chemistry = int(input("Enter your chemistry marks: "))  # str => int
physics = int(input("Enter your physics marks: "))  # "98"
biology = int(input("Enter your biology marks: "))
math = int(input("Enter your math marks: "))
total_marks = chemistry + physics + biology + math
average = total_marks / 4

print(f'chemistry = {chemistry}, physics = {physics}, biology = {biology}, math = {math}, average = {average}')
print(f"total marks= {total_marks}" )
if total_marks >= 80 :
    print("Your grade is A")
elif total_marks >= 70 :
    print("Your grade is B")
else:
    print("Your grade is C")
    