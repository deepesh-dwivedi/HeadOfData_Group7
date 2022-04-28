import re
from bs4 import BeautifulSoup
import glob
import os
import json
import datetime

files = glob.glob("/Users/abhishektiwari/Documents/GitHub/HeadOfData_Group7/deliveroo/*.html")

#order datetime
def order_datetime(x):
  datetime_str = os.path.basename(x)
  date_str = datetime_str.split("_.html")[0].replace("_", " ")
  return str(datetime.datetime.strptime(date_str, "%a %d %b %Y %H %M %S"))

#order number
def order_no(x):
  file = open(f'{x}')
  data = file.read()
  soup = BeautifulSoup(data,'html.parser')
  soup.prettify()
  subclasses = soup.find_all('h2',{"class":"vmarg16x"})[2].text
  number=""
  for i in subclasses:
    if(i.isdigit()):
      number += i
  file.close()
  return number


#delivery fee
def delivery_fee(x):
  file = open(f'{x}')
  data = file.read()
  soup = BeautifulSoup(data, 'html.parser',from_encoding='utf-8')
  soup.prettify()
  subclasses = soup.find_all('td')
  txt=[]
  for i in subclasses:
    txt.append(i.text.strip())
  i=0
  for t in txt:
    if(t=="Frais de livraison" or t=="Frais de service"):
      break
    i+=1
  file.close()
  return txt[i+1].replace('€','')
  #return re.sub(r'[^\w]', '.', txt[i+1])

#order total
def order_total(x):
  file = open(f'{x}')
  data = file.read()
  soup = BeautifulSoup(data, 'html.parser',from_encoding='utf-8')
  soup.prettify()
  subclasses = soup.find_all('td')
  txt=[]
  for i in subclasses:
    txt.append(i.text.strip())
  i=0
  for t in txt:
    if(t=="Total"):
      break
    i+=1
  file.close()
  return txt[i+1].replace('€','')
  #return re.sub(r'[^\w]', '.',txt[i+1])

def order_dict(x):
  dict={}

  if(order_datetime(x)!=""):
    dict["order"]=order_datetime(x)
  if(order_no(x)!=""):
    dict["order_number"]=order_no(x)
  if(delivery_fee(x)!=""):
    dict["delivery_fee"]=delivery_fee(x)
  if(order_total(x)!=""):
    dict["order_total_paid"]=order_total(x)

  return dict

#restaurant
def rest_details(x):
  file = open(f'{x}')
  data = file.read()
  soup = BeautifulSoup(data, 'html.parser',from_encoding='utf-8')
  soup.prettify()
  subclasses = soup.find_all('table', {"class": "fluid", "align": "left"})
  txt = subclasses[0].find_all("p")
  rest_list=[]
  for i in txt:
   rest_list.append(re.sub(r'[^\w]', ' ',i.get_text()).strip())
  file.close()

  return rest_list

def rest_dict(x):
  rest=rest_details(x)
  dict={}
  if(rest[0]!=""):
    dict["name"]=rest[0]
  if(rest[1]!=""):
    dict["address"]=rest[1]
  if(rest[2]!=""):
    dict["city"]=rest[2]
  if(rest[3]!=""):
    dict["postcode"]=rest[3]
  if(rest[4]!=""):
    dict["phone_numnber"]=rest[4]
  return dict

def customer_details(x):
  file = open(f'{x}')
  data = file.read()
  soup = BeautifulSoup(data, 'html.parser',from_encoding='utf-8')
  soup.prettify()
  subclasses = soup.find_all('table', {"class": "fluid", "align": "left"})
  txt = subclasses[2].get_text().split('\n')
  txt = list(filter(None, txt))
  fin=[]
  for i in txt:
    fin.append(re.sub(r'\ {2,}', '', re.sub(r'[^\w]', ' ',  i)))
  fin = list(filter(None, fin))
  file.close()
  return fin

def cust_dict(x):
  cust=customer_details(x)
  dict={}
  if(cust[0]!=""):
    dict["name"]=cust[0]
  if(cust[1]!=""):
    dict["address"]=cust[1]
  if(cust[2]!=""):
    dict["city"]=cust[2]
  if(cust[3]!=""):
    dict["postcode"]=cust[3]
  if(cust[4]!=""):
    dict["phone_numnber"]=cust[4]
  return dict

def order_items(x):
  file = open(f'{x}')
  data = file.read()
  soup = BeautifulSoup(data, 'html.parser',from_encoding='utf-8')
  soup.prettify()
  table = soup.find('table',{"role":"listitem"})
  all_td = table.find_all('td', {"style": "padding:0 0 16px 0;"})
  items = []
  for i in all_td:
    items.append(i.find('p').text.strip())

  final_list =[]
  name=""
  qty=""
  for i in range(len(items)):
    dict = {"name": "", "quantity": "", "price": ""}
    if (i % 3 == 0):
      qty = re.sub(r'[^\w]', ' ', items[i])
    elif(i%3==1):
      name = items[i]
    elif(i%3==2):
      dict["price"] = items[i].replace('€','').replace('\xa0', ' ')
      dict["name"]=name
      dict["quantity"]=qty
      final_list.append(dict)
  file.close()

  return final_list

file1=[]

order_df = {"order": order_dict(files[0]), "restaurant": rest_dict(files[0]), "customer": cust_dict(files[0]), "order_items": order_items(files[0])}

file1.append(order_df)
#with open("data.json", "w") as outfile:
 # json.dump(order_df,outfile)

for x in files[1:]:
  #if order_datetime(x)=="Sun_22_Nov_2020_19_07_23_" or order_datetime(x)=="Fri_26_Mar_2021_19_56_07_":
   # continue
  order_df = {"order": order_dict(x), "restaurant": rest_dict(x), "customer": cust_dict(x), "order_items": order_items(x)}
  file1.append(order_df)

with open("data.json",mode="w") as outfile:
  json.dump(file1,outfile, ensure_ascii=False)





