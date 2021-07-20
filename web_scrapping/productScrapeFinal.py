#To scrape out only one weight,price(final)...

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import boto3
import os



def ProductScrape(url): 
    try:
        html=requests.get(url).text
        soup = BeautifulSoup(html,'lxml')
        comp_name='TenderCuts'
        df=pd.read_csv("c:/python_projects/fipola/cc_result.csv",index_col=False)
        product_code=df['Product Code'].to_list()
        title=[]
        for name in soup.find_all("h3",class_="product-name"):
            title.append(name.text)
        price=soup("app-price-display")
        net_price=[re.sub("[^0-9Starts fromto\t]","",price[k].get_text()) for k in range(len(price)) if price[k] not in price[k+1:]]
        prRX=re.compile(r"[0-9]+")
        totalPrice=[]
        amount=[]
        for netPrice in net_price:
            prObjs=prRX.findall(netPrice)
            totalPrice.append(prObjs[-1])
            amount.append(totalPrice[0])
        gross_weight=[]
        net_weight=[]
        total_weight=[]
        temp=[]
        weight=soup.find("span",class_="callout")
        if weight.text.startswith("Gross"):
            uom=re.split(" ",weight.text)[5]
            grossRegex=re.compile(r"(\d)+\s-\s(\d)+")
            gross=grossRegex.search(weight.text)
            gross_weight.append(gross.group())
            df1=pd.DataFrame(data=list(zip(product_code,gross_weight,amount)),columns=['Product Code','Gross Weight','Price'])
            df1['Name'] = comp_name
            df1['Unit Of Measurement'] = uom
            df1=df1[['Name','Product Code','Gross Weight','Unit Of Measurement','Price']]
        if weight.text.startswith("Net"):
            netRegex=re.compile(r"(\d)+\s-\s(\d)+")
            net=netRegex.search(weight.text)
            net_weight.append(net.group())
            df1=pd.DataFrame(data=list(zip(product_code,net_weight,amount)),columns=['Product Code','Net Weight','Price'])
            df1['Name'] = comp_name
            df1['Unit Of Measurement'] = uom
            df1=df1[['Name','Product Code','Net Weight','Unit Of Measurement','Price']]
        elif weight.text.startswith("Weight"):
            temp.append(weight.text.split(" ")[-1])
            uom=temp[0]
            weightRegex=re.compile(r"((\d)+\s-\s(\d)+)?(\d)")
            total=weightRegex.search(weight.text)
            total_weight.append(total.group())
            df1=pd.DataFrame(data=list(zip(product_code,total_weight,amount)),columns=['Product Code','Weight','Price']) 
            df1['Name'] = comp_name
            df1['Unit Of Measurement'] = uom
            df1=df1[['Name','Product Code','Weight','Unit Of Measurement','Price']]
        print(df1)
    except Exception as e:
        print("error")