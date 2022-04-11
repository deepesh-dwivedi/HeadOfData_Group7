import re

file = open("/Users/abhishektiwari/Documents/GitHub/HeadOfData_Group7/deliveroo/Fri_01_Nov_2019_12_00_40_.html","r")
data=file.read()
file.close()


def regphone(x):
    result = re.findall(r'\+33 [6|7] \d{2} \d{2} \d{2} \d{2}', x)
    for rez in result:
        print(rez)

r = regphone(data)


