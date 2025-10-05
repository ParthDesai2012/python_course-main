list1 = [4, 5, 1, 2, 9, 7, 100, 8]
print("Original List:", list1)
sum = 0
for i in list1:
    sum += i
avg = sum/len(list1)
print("Sum =", sum)
print("Average =", avg)
#list1.sort()
print("Smallest element is:", min(list1))
print("Largest element is:", max(list1))
