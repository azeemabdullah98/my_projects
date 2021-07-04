from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import os
import json

start_url="https://tendercuts.in"
source= requests.get(start_url).text

soup = BeautifulSoup(source,'lxml')
#print(soup.prettify())
summary=soup.find('div',class_="col-3 transition ng-star-inserted")
src_link=summary.find('img')['src']
#print(src_link)
keyword=src_link.split("/")
urlword=keyword[3]
category_url=start_url+"/"+urlword
product_names=['dry','combo-packs','chicken','mutton','sea-food','marinades','cold-cuts','egg','pickle','spices','party-pack','oils']
json_files=[]
for i in range(len(product_names)):
    complete_url=category_url+"/"+product_names[i]
    product_link=requests.get(complete_url).text
    soup=BeautifulSoup(product_link,'lxml')
    name=soup.find_all("mat-card-title")
    productList=[name[x].text for x in range(len(name)) if name[x] not in name[x+1:]]    
    weight=soup("mat-card-content")
    net_weights=[]
    for k in range(len(weight)):
        weights=weight[k].get_text().replace("\n","")
        net_weights.append(re.sub("[:\s]","",weights))
    price=soup("app-price-display")
    net_price=[re.sub("[^0-9Starts fromto]","",price[k].get_text()) for k in range(len(price)) if price[k] not in price[k+1:]]
    for items in range(len(productList)):
        data={product_names[i]:[
            {"Name":productList[items],
            "Net Weight":net_weights[items],
            "Net Price":net_price[items],
        }
    ]
        }
        json_files.append(data)
with open("/mnt/c/python_projects/json_files/tender.json","a+") as f:
    json.dump(json_files,f,indent=2)
        #path="/mnt/c/python_projects/json_files/tendercuts.json"
        #if os.path.isfile == True:
           # with open(path,"a+") as f:
              #  json.dump(data,f)
        #else:
            #with open(path,'w') as f:
               # json.dump(data,f)


        
