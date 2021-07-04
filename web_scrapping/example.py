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
priceRX=re.compile("[0-9]+")
product_names=['dry','combo-packs','chicken','mutton','sea-food','marinades','cold-cuts','egg','pickle','spices','oils','sauces-spreads']
for i in range(len(product_names)):
    complete_url=category_url+"/"+product_names[i]
    product_link=requests.get(complete_url).text
    soup=BeautifulSoup(product_link,'lxml')
    name = soup("mat-card-title")
    product=[]
    for j in range(len(name)):
        product.append(name[j].string)
    product_name=[product[x] for x in range(len(product)) if product[x] not in product[x+1:]]
    weights=[]
    try:
        for weight in soup.find_all("span",class_="callout"):
            weights.append(weight.text.replace("\n",""))
        gross_weight=[]
        net_weight=[]
        for w in weights:
            if w.startswith("Gross"):
                gross_weight.append(w)
            elif w.startswith("Net") or w.endswith(" Customizable"):
                net_weight.append(w)
    except:
        weights.clear()
        for weight in soup.find_all("span",class_="callout"):
            weights.append(weight.text.replace("\n",""))
    price=soup("app-price-display")
    net_price=[re.sub("[^0-9Starts fromto\t]","",price[k].get_text()) for k in range(len(price)) if price[k] not in price[k+1:]]
    prRX=re.compile(r"[0-9]+")
    totalPrice=[]
    for netPrice in net_price:
        prObjs=prRX.findall(netPrice)
        totalPrice.append(prObjs[-1])
    df1=pd.read_csv("/mnt/c/Users/Azeem/Downloads/CC_20210505.csv",index_col=False)
    product_code=df1.loc[:,"Product Code"]
    product_code=product_code.to_list()
    access_ID=comp_name+"/"+product_names[i]+"/"+str(product_code[i])
    if len(net_weight) == len(product_name):
        df=pd.DataFrame(data=list(zip(product_name,gross_weight,net_weight,totalPrice)),columns=['Product Name','Gross Weight','Net Weight','Price'])
        df['Access ID'] = access_ID
        df['Category'] = product_names[i]
        df['Competitor Name'] = comp_name
        df['Unit of Measurement'] = 'gm'
        df=df[['Competitor Name','Access ID','Category','Product Name','Gross Weight','Net Weight','Price','Unit of Measurement']]
    else:
        df=pd.DataFrame(data=list(zip(product_name,weights,totalPrice)),columns=['Product Name','Weight','Price'])
        df['Access ID'] = access_ID
        df['Category'] = product_names[i]
        df['Competitor Name']=comp_name
        df['Unit of Measurement'] = 'gm'
        df=df[['Competitor Name','Access ID','Category','Product Name','Weight','Price','Unit of Measurement']]
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