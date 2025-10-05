# text = "Hello, World!"  # [start : stop : step]
      # 0123456     12
# print(text[-6])

# Basic slicing
# print(text[::])        # Hello, World!   -> Full string
# print(text[::1])       # Hello, World!   -> Same as above
# print(text[::-1])      # !dlroW ,olleH   -> Reversed string
# print(text[::2])       # Hlo ol!         -> Every 2nd character
# print(text[::3])       # Hl,Wl           -> Every 3rd character

# # Slicing with start and step
# print(text[1::2])      # el,Wrd          -> From index 1, every 2nd character
# print(text[2::3])      # l ,l            -> From index 2, every 3rd character

text = "Hello, World!"  
#       # 0123456     12

# # Slicing with end and step
# print(text[:5:2])      # Hlo             -> Up to index 5 (exclusive), every 2nd character
print(text[:8:3])      # Hl,             -> Up to index 8, every 3rd character

# Slicing with start, end, and step
print(text[1:10:3])    # eoo             -> From index 1 to 10 (exclusive), every 3rd character
print(text[7:1:-1])    # ,oW ol          -> From index 7 to 2 (not including), step -1
print(text[12:0:-2])   # !o,Wl           -> From index 12 to 1, step -2

# Empty results
print(text[5:2])       #                 -> No output because default step is +1 but start > end
print(text[2:5:-1])    #                 -> No output because step is -1 but start < end
