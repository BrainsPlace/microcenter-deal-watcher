import urllib.request, json 
import requests
from bs4 import BeautifulSoup
import csv
#openBox = 'https://www.microcenter.com/search/search_results.aspx?N=4294966998&prt=clearance&feature=840538&page='
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

def contains(item):
    for d in discounts:
        if str(d.id) == str(item):
            return True
    return False

def getDiscounts(url):
    print(url)
    page = requests.get(url)
    #page = requests.get(openBox + str(pageNumber))
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # LOG SOURCE PAGE IF NEEDED
    # f = open('index.html', 'w+')
    # f.write(soup.prettify())
    # f.close
    
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

readDataFile()
urls = readUrlFile()

for url in urls:
    getDiscounts(url)

data = ''   #for .csv
output = '' #for email

for d in sorted(discounts, key=lambda item: item.discountAmount, reverse=True):
    # print(d.id)
    # print(d.link)
    # print('Price    $ ' + str(d.price))
    # print('Discount $ ' + str(d.discountAmount)[:4] + ' off')
    # print('Percent    ' + str(d.discountPercent) + '% off\n')
    
    data += str(d.id) + ',' + str(d.price) + ',' + str(d.discountAmount) + ',' + str(d.discountPercent) + ',' +  d.link + ',' + str(d.newlyFound) + '\n'
    if d.newlyFound == 1:
        output += d.link + '<br>Price: $' + str(d.price) + '<br>Discount Amount: $' + str(d.discountAmount)[:4] + '<br>Discount Percent: ' + str(d.discountPercent)[:5] + '<br><br>'  

print(output)

f = open('data.csv', 'w+')
f.write(data)
f.close

if len(output) > 10:
    report = {}
    report["value1"] = output
    requests.post('https://maker.ifttt.com/trigger/discount_found/with/key/fjwO5YbabWCSy5SN4xXnZeWMzSckF0wP2B9wQCQYOsj', data=report)
else:
    print('no new items found')
    
   
    