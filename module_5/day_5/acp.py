from abc import ABC, abstractmethod

class Cars(ABC):
    def fuel_type(self):
        pass
    def max_speed(self):
        pass
class Farrari(Cars):
    def fuel_type(self):
        print("Diesel")
    def max_speed(self):
        print(1000)
class BMW(Cars):
    def fuel_type(self):
        print("Patrol")
    def max_speed(self):
        print(900)

R = Farrari()
R.fuel_type()
R.max_speed()
K = BMW()
K.fuel_type()
K.max_speed()