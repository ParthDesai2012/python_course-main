class Circle:
    def __init__(self):
        self.r = int(input("Enter the radius: "))

    def area(self):
        return 3.14 * self.r * self.r

    def perimeter(self):
        return 2 * 3.14 * self.r

c = Circle()
print("Area:", c.area())
print("Perimeter:", c.perimeter())