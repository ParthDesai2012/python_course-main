weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in meters: "))
bmi = weight / height**2
print(F"Your BMI is {bmi}")
if bmi < 18.5 :
    print("You are underweight")
elif bmi >= 18.5 and bmi < 25:
    print("Your weight is normal")
elif bmi >= 25 and bmi < 30:
    print("You are over weghit")
elif bmi >= 30:
    print("You are obese")