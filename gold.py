import requests
from bs4 import BeautifulSoup
import time
from tele_alert import make_alert, send_alert

GOLD_REF = 1900.00
PX_OFFSET_PERCENT = 0.25

def update_percent(value):
    global PX_OFFSET_PERCENT
    PX_OFFSET_PERCENT = value

def update_ref(value):
    global GOLD_REF
    GOLD_REF = value

def get_percent():
    return PX_OFFSET_PERCENT

def get_ref():
    return GOLD_REF

def extract_gold_buy(tag):
    return float(tag
                .find('div', 'textquote__row textquote__row--bid-ask')
                .find('div', 'textquote__value2')
                .text.replace(',', ''))
def get_gold():
    res = requests.get('https://goldseek.com/')
    soup = BeautifulSoup(res.content, 'html.parser')
    cur_gold = 0.0
    for tag in soup.find_all('div', 'textquote'):
        if tag.has_attr('data-symbol') and tag.attrs['data-symbol'] == 'XAUUSD':
            cur_gold = extract_gold_buy(tag)
    return cur_gold

def analyse():
    global GOLD_REF
    cur_gold = get_gold()
    change = 100 - 100 * cur_gold / GOLD_REF
    if change > PX_OFFSET_PERCENT:
        send_alert([make_alert('Gold Price dropped {:.2f}% from {}: {}'.format(change, GOLD_REF, cur_gold))])
        GOLD_REF = cur_gold
    elif change < -PX_OFFSET_PERCENT:
        send_alert([make_alert('Gold Price rised {:.2f}% from {}: {}'.format(-change, GOLD_REF, cur_gold))])
        GOLD_REF = cur_gold

def main():
    while True:
        get_gold()
        
        time.sleep(30)

if __name__ == '__main__':
    main()
