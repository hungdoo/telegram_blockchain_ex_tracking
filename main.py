# Simple python websocket client
# https://github.com/websocket-client/websocket-client

import sys
import time

import gold
import btc
from tele_alert import make_alert, send_alert
import tele_command
from logger import get_logger

logg = get_logger('ws_trade')



def do_command(command):
    try:
        tele_command.get_latest_command_from_telegram(command)
        if command.is_new:
            logg.info('Process new command: {}:{}'.format(command.type, command.value))

            if command.type == tele_command.UPDATE_REF:
                btc.update_ref(command.value)
                send_alert([make_alert(f'BTC Ref updated: {btc.get_ref()}')])
                
            elif command.type == tele_command.UPDATE_OFFSET:
                btc.update_percent(command.value)
                send_alert([make_alert(f'BTC Offset updated: {btc.get_percent()}%')])

            elif command.type == tele_command.GET_PRICE:
                    price = btc.get_btc()["last"]
                    send_alert([make_alert(f'BTC Price: {price}')])
                    
            elif command.type == tele_command.ALERT_AT:
                btc.update_alert(command.value)
                btc.alerted_reset()
                send_alert([make_alert('Alert updated: {}'.format(btc.get_alert()))])
                
            elif command.type == tele_command.LIST_CMD:
                send_alert([make_alert(', '.join(tele_command.VALID_COMMANDS.keys()))])
                
            elif command.type == tele_command.GET_INFO:
                send_alert([make_alert(f'BTC Ref/offset:{btc.get_ref()}/{btc.get_percent()}%, \
                                        Alert:{btc.get_alert()}, GOLD Ref/Off:{gold.get_ref()}/{gold.get_percent()}')])

            elif command.type == tele_command.GET_GOLD:
                send_alert([make_alert(f'Gold price: {gold.get_gold()}')])

            elif command.type == tele_command.UPDATE_GOLD_REF:
                gold.update_ref(command.value)
                send_alert([make_alert(f'Gold Ref updated: {gold.get_ref()}')])

            elif command.type == tele_command.UPDATE_GOLD_OFFSET:
                gold.update_percent(command.value)
                send_alert([make_alert(f'Gold Offset updated: {gold.get_percent()}%')])

            command.is_new = False

    except Exception as e:
        send_alert([make_alert('do_command: {}'.format(e.args))])
        logg.error('do_command: {}'.format(e.args))

def main():
    try:
        # Init command polling channel
        command = tele_command.Command()

        while True:
            # Obtain & analyse price info
            # subscribe(px_channel)
            btc.analyse()
            gold.analyse()

            # Listen & conduct commands sent from telegram
            do_command(command)
            
            time.sleep(15)

    except KeyboardInterrupt as e:
        logg.warning('main - KeyboardInterrupt')
        sys.exit(-1)

if __name__ == "__main__":
    main()
