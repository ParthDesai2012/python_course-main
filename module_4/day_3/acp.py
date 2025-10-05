key1 = input("Enter the first key:- ")
value1 = input("Enter the value for the first key:- ")
key2 = input("Enter the second key:- ")
value2 = input("Enter the value for the second key:- ")
key3 = input("Enter the third key:- ")
value3 = input("Enter the value for the third key:- ")
key4 = input("Enter the fourth key:- ")
value4 = input("Enter the value for the fourth key:- ")
key5 = input("Enter the fifth key:- ")
value5 = input("Enter the value for the fifth key:- ")
test_dict = {key1: value1, key2: value2, key3: value3, key4: value4, key5: value5}
print("The original dictionary : " + str(test_dict))
k = input("Enter the value to search:- ")
res = 0
for key in test_dict:
    if test_dict[key] == k:
        res = res + 1
print("Frequency of", k, "is:-", res)