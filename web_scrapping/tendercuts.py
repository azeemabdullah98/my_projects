from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import os

start_url="https://tendercuts.in"
comp_name=start_url.split(".")[0]
comp_name=comp_name.split("/")[2]
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
for i in range(len(product_names)):
    complete_url=category_url+"/"+product_names[i]
    product_link=requests.get(complete_url).text
    soup=BeautifulSoup(product_link,'lxml')
    name = soup("mat-card-title")
    product=[]
    for j in range(len(name)):
        product.append(name[j].string)
    product_name=[product[x] for x in range(len(product)) if product[x] not in product[x+1:]]
    weight=soup("mat-card-content")
    net_weights=[]
    for k in range(len(weight)):
        weights=weight[k].get_text().replace("\n","")
        net_weights.append(re.sub("[^gms\t-a-zA-Z]","",weights))
    price=soup("app-price-display")
    net_price=[re.sub("[^0-9Starts fromto]","",price[k].get_text()) for k in range(len(price)) if price[k] not in price[k+1:]]
   
    df=pd.DataFrame(data=list(zip(product_name,net_weights,net_price,product_names[i])),columns=['Product Name','Weight','Price','Category'])
    df['Competitor Name']=comp_name
    df=df[['Competitor Name','Product Name','Weight','Price']]
    path=f'/mnt/c/python_projects/tendercuts/tc1.csv'
    if os.path.isfile(path)==True:
        file=pd.read_csv(path)
        data=pd.concat([file,df],ignore_index=True)
        data.to_csv(path,index=False)
    else:
        print("creating new file...")
        df.to_csv(path,index=False)   
print("Done!!!")
 #Link=[product_name[i].replace(" ","-") for i in range(len(product_name))]
    #product_url=[start_url+"/product/"+Link[i] for i in range(len(Link))]