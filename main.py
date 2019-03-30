import urllib.request, json 
import requests
from bs4 import BeautifulSoup
import time
openBox = 'https://www.microcenter.com/search/search_results.aspx?N=4294966998&prt=clearance&feature=840538'

discounts = []
class Item:
    def __init__(self, link, price, discountPercent, discountAmount):
        self.link = link
        self.price = price
        self.discountPercent = discountPercent
        self.discountAmount = discountAmount
def getOpenBox():
    page = requests.get(openBox)
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
                        item = Item('https://www.microcenter.com'+i.a['href'], now,  str(discountPercent*100)[:4], discountAmount)
                        discounts.append(item)
                
        except:
            print('exception')
    

#################################################
#################################################
#################################################


f = open('index.html', 'w+')
f.write(str(getOpenBox()))
f.close

for d in sorted(discounts, key=lambda item: item.discountPercent, reverse=True):
    print(d.link)
    print('Price    $ ' + str(d.price))
    print('Discount $ ' + str(d.discountAmount)[:4] + ' off')
    print('Percent    ' + d.discountPercent + '% off\n')
    