class Dog:
    species = "Dog"
    def __init__(self, breed, name, age):
        self.breed = breed
        self.age = age
        self.name = name
Golden_Retriever = Dog("Golden Retriever", "Goldie", 10)
Poodle = Dog("Poodle", "Poodie", 13)
print("The first breed is a {}".format(Golden_Retriever.breed))
print("It's name is {}. He is {} years old".format(Golden_Retriever.name, Golden_Retriever.age))
print("The second breed is a {}".format(Poodle.breed))
print("It's name is {}. She is {} years old".format(Poodle.name, Poodle.age))