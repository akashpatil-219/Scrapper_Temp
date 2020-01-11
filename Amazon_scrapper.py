#https://hackernoon.com/scraping-amazon-product-information-with-python-and-beautifulsoup-yn4s3tgr

import requests
import json
import requests
from lxml import html
import requests.packages.urllib3.exceptions
from urllib3.exceptions import InsecureRequestWarning
import urllib3
from lxml import etree
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
url = 'file:///home/dell/GS/sampled_files/264.html'

def getDetails(url):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False, headers=headers)
    response = requests.get(url, headers=headers)
    #print(response.text)
    soup = BeautifulSoup(response.content, features="lxml")
    soup2=BeautifulSoup(response.content,"html.parser")

    containers1 = soup2.findAll("li", {"class":"s-result-item s-result-card-for-container a-declarative celwidget "})
    print("containers style 1: ", len(containers1))

    #page could be styled different, invoke query second style
    containers2 = soup2.findAll("li", {"class":"s-result-item s-result-card-for-container s-carded-grid celwidget "})
    print("containers style 2: ", len(containers2))

    #check for sponsored containers
    sponsored_containers = soup2.findAll("li", {"class":"s-result-item celwidget AdHolder"})
    print("containers style 3 sponsored: ", len(sponsored_containers))

    #check for the most common style
    common_containers = soup2.findAll("li", {"class":"s-result-item celwidget "})
    print("containers style 4 common: ", len(common_containers))

    #check for special style
    containers3 = soup2.findAll("li", {"class":"s-result-item s-col-span-12 celwidget "})
    print("containers style 5 special", len(containers3))

    title = soup.select("#productTitle")[0].get_text().strip()
    #print(title)
    ASIN=[]

    for i in soup2.findAll('div',attrs={'class':['sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28','sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 AdHolder sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28']}):
        ASIN.append(i['data-asin'])

    for i in soup2.findAll("li", {"class":"s-result-item celwidget "}) :
        ASIN.append(i['data-asin'])

    for i in soup2.findAll("li", {"class":"s-result-item celwidget AdHolder"}):
        ASIN.append(i['data-asin'])
        print(i['data_asin'])
        print('hello')
    Review_keywords=[]

    categories = []
    if(soup.select("#wayfinding-breadcrumbs_container ul.a-unordered-list")):
        for li in soup.select("#wayfinding-breadcrumbs_container ul.a-unordered-list")[0].findAll("li"):
            categories.append(li.get_text().strip())
    #price = soup.select("#priceblock_saleprice")[0].get_text()
    review_count = (soup.select("#acrCustomerReviewText")[0].get_text().split()[0])

    features = []
    for li in soup.select("#feature-bullets ul.a-unordered-list")[0].findAll('li'):
        features.append(li.get_text().strip())

    #print(price)
    #print(categories)
    #print(features)

    jsonObject = {'ASIN':ASIN,'title': title, 'categories': categories, 'features': features, 'review_count': review_count,}
    print(json.dumps(jsonObject, indent=2))
    return jsonObject

if __name__ == '__main__':
    getDetails(url)
