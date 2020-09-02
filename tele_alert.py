
import requests
import json
from logger import get_logger

logg = get_logger('ws_trade')


class Alert():
    def __init__(self, message):
        self.labels = {'name': 'hungdong-pc'}
        self.annotations = {'description': message}
    
    def dict_dumps(self):
        return {'labels':self.labels, 'annotations':self.annotations}


def make_alert(message):
    return Alert(message)

def send_alert(alerts):
    data = dict()
    data['alerts'] = [alert.dict_dumps() for alert in alerts]
    requests.post(url='http://localhost:9229/alert', data=json.dumps(data))

