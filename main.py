import urllib.request, json 
import requests
from bs4 import BeautifulSoup
import csv
openBox = 'https://www.microcenter.com/search/search_results.aspx?N=4294966998&prt=clearance&feature=840538&page='

discounts = []
class Item:
    def __init__(self, id, price, discountPercent, discountAmount, link):
        self.id = id
        self.link = link
        self.price = price
        self.discountPercent = discountPercent
        self.discountAmount = discountAmount


def readFile():
    # f = open('data.csv', 'r')
    # for line in f:
    #     print(line)
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            discounts.append(Item(row[0], row[1], row[2], row[3], row[4]))

def getOpenBox():
    pageNumber = 0
    while pageNumber < 1:
        pageNumber += 1
        print(openBox+ str(pageNumber))
        page = requests.get(openBox + str(pageNumber))
        soup = BeautifulSoup(page.text, 'html.parser')
        

        f = open('index.html', 'w+')
        f.write(soup.prettify())
        f.close
        
        for i in soup.find_all('div', {'class': 'price_wrapper'}):
            try:
                if i.div.span is not None and i.div.strong is not None:

                    original = str(i.div.span.text)
                    now = str(i.div.strong.text)

                    if len(original) > 0 and len(now) > 0:

                        original = float(original[5:].replace(',',''))
                        now = float(now[1:].replace(',',''))
                        
                        discountPercent = 1 - now/original
                        discountAmount = original - now
                        if(discountPercent > .21):
                            item = Item(i.a['href'][9:15], now, str(discountPercent*100)[:4], discountAmount, 'https://www.microcenter.com'+i.a['href'])
                            discounts.append(item)
                    
            except:
                print('exception')
    
    

#################################################
#################################################
#################################################

readFile()

# getOpenBox()
# output = ''


for d in sorted(discounts, key=lambda item: item.discountAmount, reverse=True):
    print(d.id)
    print(d.link)
    print('Price    $ ' + str(d.price))
    print('Discount $ ' + str(d.discountAmount)[:4] + ' off')
    print('Percent    ' + d.discountPercent + '% off\n')
    
#     output += str(d.id) + ',' + str(d.price) + ',' + str(d.discountAmount) + ',' + d.discountPercent + ',' +  d.link + '\n'

# f = open('data.csv', 'w+')
# f.write(output)
# f.close
    
   

    