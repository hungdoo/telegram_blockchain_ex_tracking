# Simple python websocket client
# https://github.com/websocket-client/websocket-client

import sys
import websocket
import api_msg
import json
import functools
import time

from tele_alert import make_alert, send_alert
import tele_command
from logger import get_logger

logg = get_logger('ws_trade')
ws = None

REFERENCE = 11800
ALERT_TARGET = 11800
SEEN_ALERT = False
SEEN_REF = False

class Channel:
    def __init__(self, sub, unsub):
        self.sub_msg = sub
        self.unsub_msg = unsub
        self.results = list()

# Decorator
def loop(n_times):
    def wraper(func):
        @functools.wraps(func)
        def wraped(channel):
            func(channel)
            for i in range(n_times):
                try:
                    result = ws.recv()
                    if 'subscribe' not in result:
                        channel.results.append(result)
                    logg.debug("{func} - res: {result}".format(func=func.__name__, result=result))
                except KeyboardInterrupt as e:
                    logg.error('{func} - {error_msg}'.format(func=func.__name__, error_msg=e.args))
                    raise KeyboardInterrupt()
                except Exception as e:
                    logg.error('{func} - {error_msg}'.format(func=func.__name__, error_msg=e.args))
                    raise Exception()
            unsubscribe(channel.unsub_msg)
            
        return wraped
    return wraper

def unsubscribe(msg):
    ws.send(json.dumps(msg))
    while True:
        result = ws.recv()
        if 'unsubscribed' in result:
            logg.debug("{func} - res: {result}".format(func=unsubscribe.__name__, result=result))
            break

@loop(2)
def subscribe(channel):
    ws.send(json.dumps(channel.sub_msg))

def get_authenticated_connection():
    global ws

    logg.debug('Get authenticated')
    url = "wss://ws.prod.blockchain.info/mercury-gateway/v1/ws"
    origin = 'https://exchange.blockchain.com'
    file = open("/home/hungdong/Workspace/secret.exchange.bc")
    key = file.read()
    file.close()

    ws = websocket.create_connection(url=url, origin=origin)
    au_msg = api_msg.AUTH
    au_msg["token"] = key

    ws.send(json.dumps(au_msg))
    result =  ws.recv()

    logg.debug(result)

def analyse_px(channel):
    if len(channel.results):
        price = json.loads(channel.results.pop(0))['price']

        # Check target alert (fluctuation 10/11800)
        global SEEN_ALERT
        if not SEEN_ALERT and abs(1 - price[4] / ALERT_TARGET) < 10/11800:
            logg.warning('Target price reached: tg/cr {}/{}'.format(ALERT_TARGET, price[4]))
            send_alert([make_alert('Target price reached: tg/cr {}/{}'.format(ALERT_TARGET, price[4]))])
            SEEN_ALERT = True


        # Evaluate changes
        change = 100 * price[4] / REFERENCE
        global SEEN_REF
        if not SEEN_REF and change <= 99:
            logg.warning('Price dropped {:.2f}% from {}: {}'.format(100-change, REFERENCE, price[1:5]))
            send_alert([make_alert('Price dropped {:.2f}% from {}: {}'.format(100-change, REFERENCE, price[1:]))])
            SEEN_REF = True
        elif not SEEN_REF and change >= 101:
            logg.warning('Price rised {:.2f}% from {}: {}'.format(change-100, REFERENCE, price[1:5]))
            send_alert([make_alert('Price rised {:.2f}% from {}: {}'.format(change-100, REFERENCE, price[1:]))])
            SEEN_REF = True
        else:
            pass

def do_command(command):
    try:
        tele_command.get_latest_command_from_telegram(command)
        if command.is_new:
            logg.info('Process new command: {}:{}'.format(command.type, command.value))

            if command.type == tele_command.UPDATE_REF:
                global REFERENCE
                REFERENCE = command.value
                send_alert([make_alert('Ref updated: {}'.format(REFERENCE))])
                
            elif command.type == tele_command.GET_PRICE_5M:
                px_channel = Channel(api_msg.PX_BTC_USD_5M, api_msg.UN_PX_BTC_USD)
                subscribe(px_channel)
                if len(px_channel.results):
                    price = json.loads(px_channel.results.pop(0))['price']
                    send_alert([make_alert('Price_5m: O_{} H_{} L_{} C_{} V_{}'.format(*price[1:]))])
                    
            elif command.type == tele_command.GET_PRICE_1D:
                px_channel = Channel(api_msg.PX_BTC_USD_1D, api_msg.UN_PX_BTC_USD)
                subscribe(px_channel)
                if len(px_channel.results):
                    price = json.loads(px_channel.results.pop(0))['price']
                    send_alert([make_alert('Price_1d: O_{} H_{} L_{} C_{} V_{}'.format(*price[1:]))])

            elif command.type == tele_command.ALERT_AT:
                global ALERT_TARGET
                ALERT_TARGET = command.value
                send_alert([make_alert('Alert updated: {}'.format(ALERT_TARGET))])
                
            elif command.type == tele_command.LIST_CMD:
                send_alert([make_alert(', '.join(tele_command.VALID_COMMANDS.keys()))])
                
            elif command.type == tele_command.CONT_ALERT:
                global SEEN_ALERT
                SEEN_ALERT = False

            elif command.type == tele_command.CONT_REF:
                global SEEN_REF
                SEEN_REF = False

            elif command.type == tele_command.GET_INFO:
                send_alert([make_alert('Ref/seen:{}/{}, Alert/seen:{}/{}'.format(REFERENCE, SEEN_REF, ALERT_TARGET, SEEN_ALERT))])

            else:
                pass

            command.is_new = False

    except Exception as e:
        send_alert([make_alert('do_command: {}'.format(e.args))])
        logg.error('do_command: {}'.format(e.args))

def main():
    try:
        get_authenticated_connection()
        
        # Init price tracking channel
        px_channel = Channel(api_msg.PX_BTC_USD_5M, api_msg.UN_PX_BTC_USD)

        # Init command polling channel
        command = tele_command.Command()

        while True:
            # Obtain & analyse price info
            subscribe(px_channel)
            analyse_px(px_channel)

            # Listen & conduct commands sent from telegram
            do_command(command)
            
            time.sleep(2)

    except KeyboardInterrupt as e:
        logg.warning('main - KeyboardInterrupt')
        ws.close()
        sys.exit(0)

    else:
        ws.close()

if __name__ == "__main__":
    main()