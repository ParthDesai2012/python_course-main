a = [1,2,3,4]
b = [1,2,3,4,5]
c = b
print(a is b)  # False, different objects
print(a is c)  # True, same object
print (b is c)  # False, different objects