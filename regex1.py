import re
from bs4 import BeautifulSoup

file = open("/Users/abhishektiwari/Documents/GitHub/HeadOfData_Group7/deliveroo/Fri_01_Nov_2019_12_00_40_.html","r")
data = file.read()

#Phone number of the client
def regphone(x):
    a=x
    pattern = "\+33 [6|7] \d{2} \d{2} \d{2} \d{2}"
    result =re.findall(pattern, a)
    return result

r = regphone(data)



#first order item
def getitems(x):
    soup = BeautifulSoup(x, 'html.parser')
    result = soup.findAll("td",{"width":"70%"})
    print(result[0].findChildren("p")[0].get_text())

getitems(data)


order_df={"order":{
    "order_datetime":,
    "order_number": ,
" delivery_fee":,
"order_total_paid":,
},
"restaurant":{"name":,
"address":,
"city:",
"postcode":,
"phone_number":,},
"customer":{"name":,
"address":,"city":,"postcode":,"phone_number":,},
"order_items":[{"name":,"quantity":,"price":},
{"name":,"quantity":,"price":},
{"name":,"quantity":,"price":}]}



