import requests
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

print("---Newegg---")
newEggURL = 'https://www.newegg.com/p/pl?N=100007709%20601357282&RandomID=32283675217917420201001091350&Order=6'
newEggPage = requests.get(newEggURL)
newEggSoup = BeautifulSoup(newEggPage.content, 'html.parser')
itemContainers = newEggSoup.find_all('div',class_='item-container')
outOfStockCount = 0
inStockCount = 0
inStockItems = []
for itemContainer in itemContainers:
    itemPromo = itemContainer.find('p',class_='item-promo')
    if itemPromo.text == 'OUT OF STOCK':
        outOfStockCount += 1
    else:
        inStockCount += 1
        inStockItems.append(itemContainer.text)


print("Out of Stock: ", outOfStockCount)
print("In Stock: ", inStockCount)
if inStockCount > 0:
    for inStockItem in inStockItems:
        print(inStockItem)



print("---Best Buy---")
bb3080Skus = '6429440,6436219,6430620,6436191,6436223,6436196,6432399,6436194,6432400,6430175,6432445,6430621,6432655,6436195,6432658'
response = requests.get('https://api.bestbuy.com/v1/products(sku in('+ bb3080Skus +'))?apiKey=Wh3PNjt4RqlHzxw90K1oF5mT')
#f = open("best_buy_response.xml", "w")
#f.write(response.text)
#f.close()


root = ET.fromstring(response.text)
bestBuyInStockCount = 0
bestBuyOutOfStockCount = 0
bestBuyInStockItems = []
for child in root:
    onlineAvailability = child.find('onlineAvailability').text
    cardName = child.find('name').text
    url = child.find('url').text
    if onlineAvailability == "false":
        bestBuyOutOfStockCount += 1
        bestBuyInStockItems.append(cardName + " | " + url)
    elif onlineAvailability == "true":
        bestBuyInStockCount += 1
        bestBuyInStockItems.append(cardName + " | " + url)
if bestBuyInStockCount > 0:
    for bestBuyItem in bestBuyInStockItems:
        print(bestBuyItem)

print("Out of Stock: ", bestBuyOutOfStockCount)
print("In Stock: ", bestBuyInStockCount)