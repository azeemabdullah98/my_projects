import requests
from bs4 import BeautifulSoup

start_url="https://www.fipola.in/"
source=requests.get(start_url).text
soup=BeautifulSoup(source,'lxml')
product_links=[]
for links in soup.find_all("div" ,class_="fivecols"):
    product_links.append(links.find("a")['href'])