from abc import ABC, abstractmethod

class Animal(ABC):
    def move(self):
        pass
class Human(Animal):
    def move(self):
        print("I can walk and run")
class Snake(Animal):
    def move(self):
        print("I can crawl")

R = Human()
R.move()
K = Snake()
K.move()