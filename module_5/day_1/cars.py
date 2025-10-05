class Car:
    wheels = 4
    def __init__(self, brand, millage, colour):
        self.brand = brand
        self.millage = millage
        self.colour = colour
car1 = Car("Mersidies", 150, "Green")
car2 = Car("Farrari", 700, "Red")
car3 = Car("Lamborghini", 1000, "Yellow")
print(car1.brand)
print(car2.millage)
print(car3.colour)