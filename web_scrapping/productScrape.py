import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from csv import DictReader, DictWriter
import csv


def ProductScrape(url):
    html=requests.get(url).text
    soup = BeautifulSoup(url,'lxml')
    for name in soup.find_all("h3",class_="product-name"):
        title=name.text
    price=soup("app-price-display")
    net_price=[re.sub("[^0-9Starts fromto\t]","",price[k].get_text()) for k in range(len(price)) if price[k] not in price[k+1:]]
    prRX=re.compile(r"[0-9]+")
    totalPrice=[]
    for netPrice in net_price:
        prObjs=prRX.findall(netPrice)
        totalPrice.append(prObjs[-1])
        amount=totalPrice[0]
    gross_weight=[]
    net_weight=[]
    total_weight=[]
    for weight in soup.find_all("span",class_="callout"):
        if weight.text.startswith("Gross"):
            gross_weight.append(weight.text)
        elif weight.text.startswith("Net"):
            net_weight.append(weight.text)
        else:
            total_weight.append(weight.text)
    field_names=['Name','Product Code','Product Name','Unit of Measurement']
    with open("/mnt/c/python_projects/fipola/cc_final.csv",'a+') as df:
        if title in df['Product Name']:
            dictWriter = DictWriter(df,)

