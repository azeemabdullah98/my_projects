import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import boto3
import os


def ProductScrape():
    client=boto3.client(aws_access_key_id='AKIA4QRJWH3PWSRX23RK',aws_secret_access_key='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',service_name='dynamodb')
    response = client.get_item(
        Key={
            'Std Text': {
                'S': 'Dry Anchovies Fish',
            },
        },
        TableName='material_master',
    )
    url=response['Item']['Std Class3']['S']
    html=requests.get(url).text
    soup = BeautifulSoup(html,'lxml')
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
    for weight in soup.find_all("span",class_="callout"):
        if weight.text.startswith("Gross"):
            gross_weight.append(weight.text)
        if weight.text.startswith("Net"):
            net_weight.append(weight.text)
            df1=pd.DataFrame(data=list(zip(title,gross_weight,net_weight,amount)),columns=['Text','Gross Weight','Net Weight','Price'])
#              return title,gross_weight,net_weight,amount
        elif weight.text.startswith("Weight"):
            total_weight.append(weight.text)
            df1=pd.DataFrame(data=list(zip(title,total_weight,amount)),columns=['Text','Weight','Price'])
#             return title,total_weight,amount
    df=pd.read_csv("c:/python_projects/fipola/cc_result.csv",index_col=False)
    dataframe=pd.concat([df,df1],axis=1)
    path="c:/python_projects/fipola/customer_competition.csv"
    if os.path.isfile(path) == True:
        file=pd.read_csv(path)
        data=pd.concat([file,df1],ignore_index=False)
#         data=pd.concat([file,df1],ignore_index=False)
        data.to_csv(path,index=False)
    else:
        dataframe.to_csv(path,index=False)