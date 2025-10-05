import random
ran_num = random.randint(1, 100)
if ran_num%2==0:
    print("it's an even number!")
else:
    print("It's an odd number!")
user_guess = int(input("Take a guess:"))
while user_guess<1 or user_guess>100:
    print("Kindly Guess a number between 1 to 100!")
    user_guess = int(input("Take a guess:"))

attempts = 0
while user_guess!=ran_num:
    attempts += 1 
    if user_guess<ran_num:
        print("You guessed to LOW, try again!")
    else:
        print("You guessed to HIGH, try again!")
    user_guess = int(input("Take a guess:"))
print(f"You guessed the correct number {ran_num}! It took you {attempts+1} attempts!")