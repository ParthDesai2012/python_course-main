chemistry = float(input("Enter your chemistry marks out of 25: "))  # str => float
physics = float(input("Enter your physics marks out of 25: "))  # "98"
biology = float(input("Enter your biology marks out of 25: "))
math = float(input("Enter your math marks out of 25: "))   # 12 + 6 + 7 + 18
full_marks = 100
total_marks = chemistry + physics + biology + math
average = total_marks / 4


# 8 / 10 * 100
percentage = total_marks / full_marks * 100

print(f'chemistry = {chemistry}, physics = {physics}, biology = {biology}, math = {math}, average = {average}')
print(percentage)
