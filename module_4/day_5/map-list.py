def find_cube(n):
    return n*n*n
list1 = [1,2,3,4,5,6]
cube_list = list(map(find_cube, list1))
print(cube_list)
zipped_list = list(zip(list1, cube_list))
# print(zipped_list)
for i in cube_list:
    print(i)
    if i == 8:
        print("found 8")
        exit()