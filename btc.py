import requests, json
from tele_alert import make_alert, send_alert
from commodity import Commodity

DEFAULT_REF = 11800.00
DEFAULT_PX_OFFSET_PERCENT = 1.0

class Btc(Commodity):
    def __init__(self, debug=False):
        default_dict = {"title": "BTC",
                        "PX_OFFSET_PERCENT": DEFAULT_PX_OFFSET_PERCENT,
                        "REFERENCE": DEFAULT_REF}
        super().__init__(default_dict)
        self._debug = debug
        print(f"DEBUG enabled: {self._debug}")

    def get_btc(self):
        res = requests.get('https://blockchain.info/ticker')
        if res.status_code == 200:
            btc = json.loads(res.text)
            return btc["USD"]   
        else:
            return 1.0

    def analyse(self):
        price = self.get_btc()["last"]
        reference = self.get_ref()
        offset = self.get_percent()

        # Evaluate changes
        change = 100 - 100 * price / reference
        if change > offset:
            if self._debug:
                print('BTC Price dropped {:.2f}% from {}: {}'.format(change, reference, price))
            else:
                send_alert([make_alert('*BTC* Price dropped *{:.2f}%* from {}: {}'.format(change, reference, price))])
            self.update_ref(price)
        elif change < -offset:
            if self._debug:
                print('BTC Price rised {:.2f}% from {}: {}'.format(-change, reference, price))
            else:
                send_alert([make_alert('*BTC* Price rised *{:.2f}%* from {}: {}'.format(-change, reference, price))])
            self.update_ref(price)


def main():
    btc = Btc(debug=True)
    print(f"DEBUG get_ref: {btc.get_ref()}")
    print(f"DEBUG get_offset: {btc.get_percent()}")
    print(f"DEBUG get_btc: {btc.get_btc()}")
    print(f"DEBUG update_ref(15000): ")
    btc.update_ref(15000)
    print(f"DEBUG update_offset(2): ")
    btc.update_percent(2)
    print(f"DEBUG get_ref: {btc.get_ref()}")
    print(f"DEBUG get_offset: {btc.get_percent()}")
    print(f"DEBUG analyse: ")
    btc.analyse()
    print(f"DEBUG update_ref(200): ")
    btc.update_ref(200)
    print(f"DEBUG analyse: ")
    btc.analyse()        

def test():
    send_alert([make_alert('`1dsada` **dasdas** `fdafasd`')])
    # send_alert([make_alert('BTC* Price dropped `{:.2f}%` from {}: {}'.format(11.2))])

if __name__ == '__main__':
    # main()
    test()
