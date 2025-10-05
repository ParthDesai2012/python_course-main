try:
    num1, num2 = eval(input("Enter two number and seperate the with a comma(,):-"))
    result = num1/num2
    print("Result is", result)
except ZeroDivisionError as zx:
    print(zx)
except SyntaxError:
    print("Comma is missing! Enter numbers seperated by a comma like this- 1, 2")
except:
    print("Wrong input")
else:
    print("No exceptions")
finally:
    print("This will execute no matter what")