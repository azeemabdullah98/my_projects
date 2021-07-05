#web scraping using BeautifulSoup and reuests packages...
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import os
#applicable only for tendercuts website...
start_url="https://tendercuts.in"
comp_name=start_url.split(".")[0] #To get the competitor name from start_url...
comp_name=comp_name.split("/")[2]
source= requests.get(start_url).text #sending request to the start_url...

soup = BeautifulSoup(source,'lxml') #parsing the html using lxml parser...
#print(soup.prettify())
summary=soup.find('div',class_="col-3 transition ng-star-inserted")#finding a particular tag in the html page...
src_link=summary.find('img')['src']
#print(src_link)
keyword=src_link.split("/")#splitting the url to get the particular word...
urlword=keyword[3]
category_url=start_url+"/"+urlword#performing string concatenation...
product_names=['dry','combo-packs','chicken','mutton','sea-food','marinades','cold-cuts','egg','pickle','spices','party-pack','oils']#list of product names to be added to the url
for i in range(len(product_names)): #looping through each product_names...
    complete_url=category_url+"/"+product_names[i] #perform string concatenation to obtain the expected product url...
    product_link=requests.get(complete_url).text #requests perform for n url where n=len(product_names)...
    soup=BeautifulSoup(product_link,'lxml')#parsing with BeautifulSoup...
    name = soup("mat-card-title") #search for title of the product...
    product=[]
    for j in range(len(name)):
        product.append(name[j].string)
    product_name=[product[x] for x in range(len(product)) if product[x] not in product[x+1:]] #to remove duplication within the product_name...
    weight=soup("mat-card-content") #search for the weight of the product...
    net_weights=[]
    for k in range(len(weight)):
        weights=weight[k].get_text().replace("\n","")
        net_weights.append(re.sub("[:A-Za-z\s]","",weights))
    price=soup("app-price-display") #search for the price of the product...
    net_price=[re.sub("[^0-9Starts fromto]","",price[k].get_text()) for k in range(len(price)) if price[k] not in price[k+1:]]
    df=pd.DataFrame(data=list(zip(product_name,net_weights,net_price)),columns=['Name','Net Weight','Selling Price'])# creating a dataframe table...
    df['Competitor Name']=comp_name
    path=f'/mnt/c/python_projects/excel/{product_names[i]}.csv'
    #To check if the file already exists or not...
    if os.path.isfile(path)==True: 
        print("file already exists...")
    else:
        print("creating new file...")
        df.to_csv(path,index=False)   
print("Done!!!")
    



    
    

#src_link=summary.find('a',class_="products-list px-3 mb-1 ng-star-inserted")['href']

#print(summary)