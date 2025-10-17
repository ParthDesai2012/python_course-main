class Vehicle:
    def __init__(self, seating_capacity):
        self.seating_capacity = seating_capacity

    def fare(self):
        return self.seating_capacity * 100


class Bus(Vehicle):
    def fare(self):
        base_fare = super().fare()
        total_fare = base_fare + (0.10 * base_fare)  # 10% maintenance charge
        return total_fare


# Example usage
bus = Bus(50)
print("Total Bus fare is:", bus.fare())
