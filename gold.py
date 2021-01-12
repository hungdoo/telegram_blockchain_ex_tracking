import requests
from bs4 import BeautifulSoup
import time
from tele_alert import make_alert, send_alert
from commodity import Commodity

DEFAULT_REF = 1900.00
DEFAULT_PX_OFFSET_PERCENT = 0.25

class Gold(Commodity):
    def __init__(self, debug=False):
        default_dict = {"title": "GOLD",
                        "PX_OFFSET_PERCENT": DEFAULT_PX_OFFSET_PERCENT,
                        "REFERENCE": DEFAULT_REF}
        super().__init__(default_dict)
        self._debug = debug
        print(f"DEBUG enabled: {self._debug}")

    def _extract_gold_buy(self, tag):
        return float(tag
                    .find('div', 'textquote__row textquote__row--bid-ask')
                    .find('div', 'textquote__value2')
                    .text.replace(',', ''))
    def get_gold(self):
        res = requests.get('https://goldseek.com/')
        soup = BeautifulSoup(res.content, 'html.parser')
        cur_gold = 0.0
        for tag in soup.find_all('div', 'textquote'):
            if tag.has_attr('data-symbol') and tag.attrs['data-symbol'] == 'XAUUSD':
                cur_gold = self._extract_gold_buy(tag)
                break
        return cur_gold

    def analyse(self):
        cur_gold = self.get_gold()
        if cur_gold == 0.0:
            return
        reference = self.get_ref()
        offset = self.get_percent()

        change = 100 - 100 * cur_gold / reference
        if change > offset:
            if self._debug:
                print('Gold Price dropped {:.2f}% from {}: {}'.format(change, reference, cur_gold))
            else:
                send_alert([make_alert('`Gold` Price dropped `{:.2f}%` from {}: {}'.format(change, reference, cur_gold))])
            self.update_ref(cur_gold)
        elif change < -offset:
            if self._debug:
                print('Gold Price rised {:.2f}% from {}: {}'.format(-change, reference, cur_gold))
            else:
                send_alert([make_alert('`Gold` Price rised `{:.2f}%` from {}: {}'.format(-change, reference, cur_gold))])
            self.update_ref(cur_gold)


def main():
    gold = Gold(debug=True)
    print(f"DEBUG get_ref: {gold.get_ref()}")
    print(f"DEBUG get_offset: {gold.get_percent()}")
    print(f"DEBUG get_gold: {gold.get_gold()}")
    print(f"DEBUG update_ref(2000): ")
    gold.update_ref(2000)
    print(f"DEBUG update_offset(1): ")
    gold.update_percent(1)
    print(f"DEBUG get_ref: {gold.get_ref()}")
    print(f"DEBUG get_offset: {gold.get_percent()}")
    print(f"DEBUG analyse: ")
    gold.analyse()
    print(f"DEBUG update_ref(200): ")
    gold.update_ref(200)
    print(f"DEBUG analyse: ")
    gold.analyse()        

if __name__ == '__main__':
    main()
