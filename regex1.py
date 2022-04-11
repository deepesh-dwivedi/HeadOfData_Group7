import re

file = open("/Users/abhishektiwari/Documents/GitHub/HeadOfData_Group7/deliveroo/Fri_01_Nov_2019_12_00_40_.html","r")

print(" step 1")
data=file.read()
print(" step 2")

file.close()


def regphone(x):
    a=x
    a=a.replace(" ","")
    pattern = "\+33[6|7]\d{8}"
    result =re.match(pattern, a)
    return result


r = regphone(data)

print(r)

