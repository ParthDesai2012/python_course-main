class Employee:

    designation = "Senior Manager"
    def __init__(self):
        print('Emplyee Created')
    def __del__(self):
        print("Destructor called")

def Creat_obj():
    print('Making object...')
    obj = Employee()
    return obj
print('Calling Create_obj() function...')
obj = Creat_obj()
print('Program End...')
print(obj.designation)
del obj
print(obj.designation)