#https://infoviumwebscraping.com/how-to-scrape-amazon-product-data-using-python/
import requests
from lxml import html
import requests.packages.urllib3.exceptions
import json
from urllib3.exceptions import InsecureRequestWarning
import urllib3
from lxml import etree

# below code send http get request to yellowpages.com
# return content in form of string
# lib Refernce
# 1 :- request

def getRequest(url):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False, headers=headers)
    return response.text

# This method is use to parse data from string
# Return object with data
# lib Refrence
# 1 :- lxml
# 2 : json

def parseData(strHtml):
    parser = html.fromstring(strHtml)

    # Parse Data Using
    URL = parser.xpath('//link[@rel=”canonical”]')[0].attrib['href']
    ASIN = parser.xpath('//div[@id=”cerberus-data-metrics”]')[0].attrib['data-asin']
    nodes = parser.xpath('//div[@class=”content”]/ul/li')
    for node in nodes:
        if 'UPC' in ".join(node.itertext()):
            UPC = ".join(node.itertext()).replace('UPC:', ”).strip()
    for node in nodes:
        if 'Item model number' in ".join(node.itertext()):
            ItemModelNumber = ".join(node.itertext()).replace('Item model number:', ”).strip()
    for node in nodes:
        if 'Average Customer Review' in ".join(node.itertext()):
            NoofReviews = ".join(node.itertext()).replace('Average Customer Review:', ”).strip()

    SalesrankFinal = ".join(parser.xpath('//ul[@class=”zg_hrsr”]')[0].itertext()).strip()
    NoofRatings = parser.xpath('//span[@id =”acrPopover”]/span[1]/a/i[1]/span')[0].text.strip()
    productDescription = ".join(parser.xpath('//div[@id=”productDescription”]')[0].itertext()).strip()
        for node in nodes:
            if 'Product Dimensions' in ”.join(node.itertext()):
                Productdimensions = ”.join(node.itertext()).replace('Product Dimensions:', ”).strip()
    BSR = parser.xpath('//li[@id=”SalesRank”]/text()')[1].strip()
    for node in nodes:
        if 'Shipping Weight' in ”.join(node.itertext()):
            ShippingWeight = ”.join(node.itertext()).replace('Shipping Weight:', ”).strip()
    Category = parser.xpath('//span[@id=”productTitle”]')[0].text.strip()
    Price = parser.xpath('//span[@class=”a-color-price”]')[0].text.strip()
    product_title = parser.xpath('//span[@id=”productTitle”]')[0].text.strip()
    #Shippingcost = parser.xpath(‘//span[@id=”ourprice_shippingmessage”]/span’)[0].text.strip()

    return {
    'URL': URL,
    'ASIN': ASIN,
    'UPC': UPC,
    'Item Model Number': ItemModelNumber,
    'No Of Reviews': NoofReviews,
    'Sales Rank Final': SalesrankFinal,
    'No Of Ratings': NoofRatings,
    'product Description': productDescription,
    'Product Dimensions': Productdimensions,
    #’Availability’: Availability,
    'Best Seller Rank': BSR,
    'Shipping Weight': ShippingWeight,
    'Category': Category,
    'Price': Price,
    'product_title': product_title
    #’Shippingcost’: Shippingcost
    }
