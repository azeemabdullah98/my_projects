import json
import requests
from bs4 import BeautifulSoup
import re
import boto3
from boto3.dynamodb.conditions import Key
import csv
from datetime import datetime


def ProductScrape(links): 
    '''Function with links as argument to scrape the Tendercuts website, convert it to csv and upload the file to s3 bucket
    and unprocessed links are stored in a separate s3 bucket in txt format'''
    
    comp_name='TenderCuts'
    s3=boto3.resource('s3')
    product_bucket=s3.Bucket('scraping.bucket.source')
    error_bucket=s3.Bucket('scraping.bucket.error')
    Key='productFile.csv'
    key='urlLinks.txt'
    outputFile=open('/tmp/output.csv', 'w+', newline='')
    outputDictWriter=csv.DictWriter(outputFile,['Name','Product Code','Weight','Gross Weight','Net Weight','Unit Of Measurement','Price'])
    outputDictWriter.writeheader()
    url_file=open('/tmp/links.txt','w+')
    for url in links:
        try:
            html=requests.get(url).text
            soup = BeautifulSoup(html,'html.parser')
            rate=soup.find("app-price-display").text.replace("\n",'')
            priceRegex=re.compile(r"[0-9]+")
            price=priceRegex.findall(rate)[-1]
            temp=[]
            weight=soup.find("span",class_="callout")
            if weight.text.startswith("Gross"):
                uom=re.split(" ",weight.text)[5]
                grossRegex=re.compile(r"(\d)+\s-\s(\d)+")
                gross=grossRegex.search(weight.text)
                gross_weight=gross.group()
                outputDictWriter.writerow({'Name':comp_name,'Product Code':' ','Weight':'-','Gross Weight':gross_weight,'Net Weight':'-','Unit Of Measurement':uom,'Price':price})
            if weight.text.startswith("Net"):
                netRegex=re.compile(r"(\d)+\s-\s(\d)+")
                net=netRegex.search(weight.text)
                net_weight=net.group()
                outputDictWriter.writerow({'Name':comp_name,'Product Code':' ','Weight':'-','Gross Weight':'-','Net Weight':net_weight,'Unit Of Measurement':uom,'Price':price})
            elif weight.text.startswith("Weight"):
                temp.append(weight.text.split(" ")[-1])
                uom=temp[0]
                weightRegex=re.compile(r"((\d)+\s-\s(\d)+)?(\d)")
                total=weightRegex.search(weight.text)
                total_weight=total.group()
                outputDictWriter.writerow({'Name':comp_name,'Product Code':' ','Weight':total_weight,'Gross Weight':'-','Net Weight':'-','Unit Of Measurement':uom,'Price':price})
        except Exception as e:
            now=datetime.now()
            current=now.strftime("%d/%m/%Y %H:%M:%S")
            url="\n"+url+"\n"
            url_file.writelines(url)
            url_file.writelines(["-> ",current])
    outputFile.close()
    url_file.close()
    product_bucket.upload_file(Filename='/tmp/output.csv',Key=Key)
    error_bucket.upload_file(Filename='/tmp/links.txt',Key=key)
    
    
    
def DBquery():
    '''Function to query from dynamodb'''
    client=boto3.resource('dynamodb')
    table=client.Table('AB00004')
    url=[]
    response=[]
    response.append(table.query(
        KeyConditionExpression=Key('PK').eq('TY#TE1#PRODCD#OneRetail#CONTXT#tendercuts')&Key('SK').eq('FPF#20210702#ACID#tendercuts/chicken/200102#TXT#Chicken Boneless (Cubes) (1 Kg)#CODE# #VER#1')))
    for i in response[0]['Items']:
        url.append(i['StdClass3'])
    ProductScrape(links=url)
    
    
    
def lambda_handler(event, context):
    DBquery()
    return {
        'statusCode': 200,
        'body': json.dumps('success')
    }
    
