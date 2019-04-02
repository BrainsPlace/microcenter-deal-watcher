# micropy

The goal of this project is to get an email via a ifttt webhook to see the most up to date deals at my local microcenter


### Files

`ifttt.txt` is a single line file that contains **your** webhook URL generated at https://ifttt.com/maker_webhooks
* ifttt message body requires `Value1` only
* recommended to turn URL shortening of at https://ifttt.com/settings
* get your custom webhook url at https://ifttt.com/services/maker_webhooks/settings

`data.csv` Holds a "database" of previously parsed deals

`urls.txt` contains a list of URLs to crawl
