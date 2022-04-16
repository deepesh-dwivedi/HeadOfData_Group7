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
    tables = soup.findAll("table",{"role":"listitem"})
    print(type(tables))
    children = tables[0].find_all("td", {"width":"70%"})
    percent_soup = BeautifulSoup(children, "html.parser")
    result = {
        row.td.get_text(strip=True): row("td")[1].get_text()
        for row in percent_soup.find_all("tr")
    }
    #result = []

    #for child in children:
    #    for temp in str(child.text).split("\n"):
    #        result.append(temp)
    #print("".join(result))
    print(len(result))

#def order_details(x):




     #   text = soup.findAll("")
    #print(result.findChildren("p").get_text())

getitems(data)


'''
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
'''


