import urllib
import json 
import requests
from bs4 import BeautifulSoup
import csv
urls = []
discounts = []

class Item:
    def __init__(self, id, price, discountPercent, discountAmount, link, newlyFound):
        self.id = id
        self.link = link
        self.price = price
        self.discountPercent = discountPercent
        self.discountAmount = discountAmount
        self.newlyFound = newlyFound


def readDataFile():
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        print('=================== LOADING ===================')
        for row in reader:
            discounts.append(Item(row[0], row[1], float(row[2]), float(row[3]), row[4], 0))
            print('adding discount: ' + str(row[0]))
        print('============== LOADING COMPLETE================')

def readUrlFile():
    with open('urls.txt', 'r') as f:
        return f.readlines()

#single line file ex: https://maker.ifttt.com/trigger/{TRIGGER NAME}/with/key/{KEY}
def readIFTTT():
    with open('ifttt.txt', 'r') as f:
        return f.readline()


def contains(item):
    for d in discounts:
        if str(d.id) == str(item):
            return True
    return False

def getDiscounts(url):
    print('getting ' + url)
    cookie = dict(storeSelected='141') #get this from your browser console > storage > cookies
    page = requests.get(url,cookies=cookie)
    soup = BeautifulSoup(page.text, 'html.parser')

    for i in soup.find_all('div', {'class': 'price_wrapper'}):
        try:
            if i.div.span is not None and i.div.strong is not None:
                id = i.a['href'][9:15]
                if not contains(id):
                    #print('Found New Item: ' + str(id))
                    original = str(i.div.span.text)
                    now = str(i.div.strong.text)

                    if len(original) > 0 and len(now) > 0:

                        original = float(original[5:].replace(',',''))
                        now = float(now[1:].replace(',',''))
                        
                        discountPercent = 1 - now/original
                        discountAmount = float(original - now)
                        if(discountPercent > .21):
                            item = Item(id, now, str(discountPercent*100)[:4], discountAmount, 'https://www.microcenter.com'+i.a['href'], 1)
                            discounts.append(item)
                
        except:
            print('exception')
    
    

#################################################
##################### MAIN ######################
#################################################

ifttt = readIFTTT()
print(ifttt)
readDataFile()
urls = readUrlFile()

for url in urls:
    getDiscounts(url)

data = ''   #for .csv
output = '' #for email

for d in sorted(discounts, key=lambda item: item.discountAmount, reverse=True):
    data += str(d.id) + ',' + str(d.price) + ',' + str(d.discountAmount) + ',' + str(d.discountPercent) + ',' +  d.link + ',' + str(d.newlyFound) + '\n'
    if d.newlyFound == 1:
        output += d.link + '<br>Price: $' + str(d.price) + '<br>Discount Amount: $' + str(d.discountAmount)[:4] + '<br>Discount Percent: ' + str(d.discountPercent)[:5] + '<br><br>'  

f = open('data.csv', 'w+')
f.write(data)
f.close

if len(output) > 10:
    report = {}
    report["value1"] = output
    print(requests.post(ifttt, data=report).text)
else:
    print('no new items found')
    
   
    