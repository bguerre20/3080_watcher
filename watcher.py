
import requests
import json
import warnings
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from twilio.rest import Client
import time

#load into our OS environment variables the entries declared in the file called .env in the same folder as this .py file
load_dotenv()

#Get our environment variables from our .env file
bbyKey = os.getenv("WATCHER_BBY_KEY")
print(bbyKey)
twilioAccountSID = os.getenv('WATCHER_TWILIO_ACCOUNT_SID')
twilioAuthToken = os.getenv("WATCHER_TWILIO_AUTH_TOKEN")
phoneNum = os.getenv('WATCHER_PHONE_NUMBER')
fromNum = os.getenv('WATCHER_TWILIO_FROM_NUMBER')
emailAddress = os.getenv('WATCHER_EMAIL_ADDRESS')


if bbyKey:
    print('bbyKey: ' + bbyKey)
else:
    print('!!!WATCHER_BBY_KEY not specified in .env BBY will be unavailable.')

if twilioAccountSID:
    print('twilioAccountSID: ' + twilioAccountSID)
else:
    print('!!!WATCHER_TWILIO_ACCOUNT_SID not specified in .env text alerts will be unavailable.')

if twilioAuthToken:
    print('twilioAuthToken: ' + twilioAuthToken)
else:
    print('!!!WATCHER_TWILIO_AUTH_TOKEN not specified in .env text alerts will be unavailable.')

if phoneNum:
    print('phoneNum: ' + phoneNum)
else:
    print('!!!WATCHER_PHONE_NUMBER not specified in .env text alerts will be unavailable.')

if fromNum:
    print('fromNum: ' + fromNum)
else:
    print('!!!WATCHER_TWILIO_FROM_NUMBER not specified in .env text alerts will be unavailable.')

if emailAddress:
    print('emailAddress: ' + emailAddress)
else:
    print('!!!WATCHER_EMAIL_ADDRESS not specified in .env email alerts will be unavailable.')

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


if bbyKey:
    print("---Best Buy---")
    bb3080Skus = '6429440,6436219,6430620,6436191,6436223,6436196,6432399,6436194,6432400,6430175'
    bbsku2 = '6432445,6430621,6432655,6436195,6432658,6429442,6437912,6439300,6437909,6429434'
    bb3080skus1 = '6429440,6430621,6432399,6430175,6430620,6432655,6436194,6432658,6432400,6436195'
    bb3080sku2 = '6436219,6436191,6436196,6436223,6432445'
    bb3070sku1 = '6429442,6437912,6439300,6432654,6432653,6437909'
    #bb3070sku2 = ''
    bb3090sku1 = '6429434,6434363,6430624,6430215,6430623,6432656,6432657,6432446,6437910,6436193'
    bb3090sku2 = '6436192,6432447'
    bbAllSku = ["6429440","6436219","6430620","6436191","6436223","6436196","6432399","6436194","6432400","6430175" ,"6432445","6430621","6432655","6436195","6432658","6429442","6437912","6439300","6437909","6429434","6429440","6430621","6432399","6430175","6430620","6432655","6436194","6432658","6432400","6436195","6436219","6436191","6436196","6436223","6432445","6429434","6434363","6430624","6430215","6430623","6432656","6432657","6432446","6437910","6436193","6436192","6432447"]
    
    skuString = ""
    skuCount = 0
    
    count = 0
    bestBuyInStockCount = 0
    bestBuyOutOfStockCount = 0
    bestBuyInStockItems = []

    for sku in bbAllSku:
        skuString = skuString + sku + ","
        skuCount = skuCount + 1
        if skuCount % 10 == 0 or skuCount == len(bbAllSku):
            skuString = skuString[:-1]
            print(skuString)
            response = requests.get('https://api.bestbuy.com/v1/products(sku in('+ skuString +'))?apiKey=' + bbyKey)
            root = ET.fromstring(response.text)
            for child in root:
                onlineAvailability = child.find('onlineAvailability').text
                cardName = child.find('name').text
                url = child.find('url').text
                count += 1
                if onlineAvailability == "false":
                    bestBuyOutOfStockCount += 1
                elif onlineAvailability == "true":
                    bestBuyInStockCount += 1
                    bestBuyInStockItems.append(cardName + " | " + url)
            skuString = ''
            time.sleep(1)

    print(count)
 
    print("Out of Stock: ", bestBuyOutOfStockCount)
    print("In Stock: ", bestBuyInStockCount)
    if bestBuyInStockCount > 0:
        for bestBuyItem in bestBuyInStockItems:
            print(bestBuyItem)   

if inStockCount > 0:
    for newEggInStockItem in inStockItems:
        client = Client(twilioAccountSID, twilioAuthToken)
        message = client.messages \
                        .create(
                            body="NewEgg 3080 in stock!" + newEggInStockItem,
                            from_=str(fromNum),
                            to=str(phoneNum)
                        )
        print(message.sid)
if bestBuyInStockCount > 0:
    for bestBuyInStockItem in bestBuyInStockItems:
        client = Client(twilioAccountSID, twilioAuthToken)
        message = client.messages \
                        .create(
                            body="BestBuy 3080 in stock!" + bestBuyInStockItem,
                            from_=str(fromNum),
                            to=str(phoneNum)
                        )
        print(message.sid)