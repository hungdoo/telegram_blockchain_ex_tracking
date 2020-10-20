import requests
import json
from tele_alert import make_alert, send_alert

REFERENCE = 11800
ALERT_TARGET = 11800
PX_OFFSET_PERCENT = 1
isALERTED = False

def alerted_reset():
    global isALERTED
    isALERTED = False

def alerted():
    global isALERTED
    isALERTED = True

def update_alert(value):
    global ALERT_TARGET
    ALERT_TARGET = value

def update_percent(value):
    global PX_OFFSET_PERCENT
    PX_OFFSET_PERCENT = value

def update_ref(value):
    global REFERENCE
    REFERENCE = value

def get_percent():
    return PX_OFFSET_PERCENT

def get_ref():
    return REFERENCE

def get_alert():
    return ALERT_TARGET

def get_btc():
    res = requests.get('https://blockchain.info/ticker')
    if res.status_code == 200:
        btc = json.loads(res.text)
    return btc["USD"]

def analyse():
    btc = get_btc()
    price = btc["last"]

    # Check target alert (fluctuation 10/11800)
    if not isALERTED and abs(1 - price / ALERT_TARGET) < 10/11800:
        send_alert([make_alert('Target price reached: tg/cr {}/{}'.format(ALERT_TARGET, price))])
        alerted()

    # Evaluate changes
    change = 100 - 100 * price / REFERENCE
    if change > PX_OFFSET_PERCENT:
        send_alert([make_alert('BTC Price dropped {:.2f}% from {}: {}'.format(change, REFERENCE, price))])
        update_ref(price)
    elif change < -PX_OFFSET_PERCENT:
        send_alert([make_alert('BTC Price rised {:.2f}% from {}: {}'.format(-change, REFERENCE, price))])
        update_ref(price)

def main():
    print(f"Debug get_btc: {get_btc()}")
    update_ref(1)
    analyse()


if __name__ == '__main__':
    main()