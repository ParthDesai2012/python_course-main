def palind(r):
    e = len(r) -1
    s = 0
    while(s<e):
        if(r[s]!=r[e]):
            return False
        s+=1
        e-=1
    return True
user_input = input("Enter a tuple (e.g., (1, 2, 3)): ")
tup = eval(user_input)
print("Your tuple:", tup)
if(palind(tup)):
    print("The tuple is a Flip-Flop!")
else:
    print("The tuplae is not a Flip-Flop!")