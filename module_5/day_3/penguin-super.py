class Bird:
    def __init__(self):
        self.can_fly = True
        self.legs = 2
    
    def info(self):
        print(f"A bird has {self.legs} legs.")

class Penguin(Bird):
    def __init__(self):
        super().__init__()
        self.can_fly = False
        self.habitat = "Cold Ocean"

    def info(self):
       super().info()
       print(f"Can fly: {self.can_fly}")
       print(f"Habitat: {self.habitat}")

peggy = Penguin()
peggy.info()