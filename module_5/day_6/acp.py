class RomanConverter:
    def __init__(self, number):
        self.number = number
    def to_roman(self):
        value_map = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
        ]

        num = self.number
        roman = ""

        for value, symbol in value_map:
            while num >= value:
                roman += symbol
                num -= value

        return roman

num = int(input("Enter a number: "))
converter = RomanConverter(num)
print("Roman Numeral:", converter.to_roman())
