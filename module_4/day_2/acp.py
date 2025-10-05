tup1 = (4, 3, 2, 2, -1, 18)
tup2 = (2, 4, 8, 8, 3, 2, 9)
def t_p(t):
    product = 1
    for num in t:
        product *= num
    return product
print("Tuple 1:", tup1)
print("Product of Tuple 1:", t_p(tup1))
print("Tuple 2:", tup2)
print("Product of Tuple 2:", t_p(tup2))