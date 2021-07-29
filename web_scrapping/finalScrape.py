#To scrape out only one weight,price from multiple URLs and to store the url which is not processed(final)...

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import boto3
import os
import csv
from datetime import datetime



def ProductScrape(links): 
    comp_name='TenderCuts'
    outputFile=open('output.csv','w+',newline='')
    outputDictWriter=csv.DictWriter(outputFile,['Name','Weight','Gross Weight','Net Weight','Unit Of Measurement','Price'])
    outputDictWriter.writeheader()
    for url in links:
        try:
            html=requests.get(url).text
            soup = BeautifulSoup(html,'lxml')
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
                outputDictWriter.writerow({'Name':comp_name,'Weight':'-','Gross Weight':gross_weight,'Net Weight':'-','Unit Of Measurement':uom,'Price':price})
            if weight.text.startswith("Net"):
                netRegex=re.compile(r"(\d)+\s-\s(\d)+")
                net=netRegex.search(weight.text)
                net_weight=net.group()
                outputDictWriter.writerow({'Name':comp_name,'Weight':'-','Gross Weight':'-','Net Weight':net_weight,'Unit Of Measurement':uom,'Price':price})
            elif weight.text.startswith("Weight"):
                temp.append(weight.text.split(" ")[-1])
                uom=temp[0]
                weightRegex=re.compile(r"((\d)+\s-\s(\d)+)?(\d)")
                total=weightRegex.search(weight.text)
                total_weight=total.group()
                outputDictWriter.writerow({'Name':comp_name,'Weight':total_weight,'Gross Weight':'-','Net Weight':'-','Unit Of Measurement':uom,'Price':price})
        except Exception as e:
            now=datetime.now()
            current=now.strftime("%d/%m/%Y %H:%M:%S")
            url="\n"+url+"\n"
            url_file=open('links.txt','a+')
            url_file.writelines(url)
            url_file.writelines(["-> ",current])
            url_file.close()
            s3=boto3.resource('s3')
            bucket=s3.Bucket('error.links')
            bucket.upload_file(Filename='links.txt',Key='url_links.txt')
    outputFile.close()
    s3=boto3.resource('s3')
    bucket=s3.Bucket('products.csv.file')
    bucket.upload_file(Filename='output.csv',Key='productScrapeFile.csv')