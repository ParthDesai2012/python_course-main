num = int(input("Enter a number divisible by 3:- "))
def divBy3(num):
    return num % 3 == 0
def findCube(num):
    return num * num * num
if divBy3(num):
    print(f"the cube of {num} is {findCube(num)}")
else:
    print(f"{num} is not divisible by 3!")