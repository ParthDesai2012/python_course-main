side1 = float(input("Enter the first side: "))
side2 = float(input("Enter the second side: "))
side3 = float(input("Enter the third side: "))
if (side1 + side2 > side3) and (side2 + side3 > side1) and (side1 + side3 > side2):
    # Check for triangle type
    if side1 == side2 == side3:
        print("The triangle is Equilateral.")
    else:
        if side1 == side2 or side2 == side3 or side1 == side3:
            print("The triangle is Isosceles.")
        else:
            print("The triangle is Scalene.")
else:
    print("The sides do not form a valid triangle.")