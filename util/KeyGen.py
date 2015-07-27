from random import random
string = ""
min = " "
max = "~"
for i in range(20):
    string += chr(int(random() * (ord(max) - ord(min))) + ord(min) )
print string
