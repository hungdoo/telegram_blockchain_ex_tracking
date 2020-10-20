import requests
import json
from logger import get_logger

logg = get_logger()

# Const
UPDATE_REF = 'upBTCRef'
UPDATE_OFFSET = 'upBTCOffset'
ALERT_AT = 'alertBTCAt'
ALERT_GOLD_AT = 'alertGoldAt'
GET_PRICE = 'getBTC'
LIST_CMD = 'ls'
GET_INFO = 'getInfo'
GET_GOLD = 'getGold'
UPDATE_GOLD_REF = 'upGoldRef'
UPDATE_GOLD_OFFSET = 'upGoldOffset'

VALID_COMMANDS = {
    # Command: value type
    UPDATE_REF: float, # Update reference/target value
    UPDATE_OFFSET: float, # Update BTC PX_OFFSET_PERCENT value
    ALERT_AT: float, # Alert at specific price
    ALERT_GOLD_AT: float, # Alert at specific price
    GET_PRICE: None, # Get current BTC price 5 min
    LIST_CMD: None, # List all avail. commands
    GET_INFO: None, # List all avail. commands
    GET_GOLD: None, # Get current GOLD price
    UPDATE_GOLD_REF: float, # Update reference/target value
    UPDATE_GOLD_OFFSET: float, # Update Gold PX_OFFSET_PERCENT value
}

class Command():
    def __init__(self):
        self.id = -1
        self.is_new = False
        self.type = None
        self.value = None # send text format <type;value>

def get_latest_command_from_telegram(command):
    res = requests.get('http://localhost:9229/noti')
    data = json.loads(res.text)
    if len(data):
        care_item = data[0]
        msg_id = care_item['message']['message_id']

        if command.id == msg_id:
            return
        else:
            command.id = msg_id

        # Check command syntax
        text = care_item['message']['text']
        if ';' in text:
            cmd_type, cmd_value = text.split(';')
            if cmd_type in VALID_COMMANDS and VALID_COMMANDS[cmd_type] is float:
                try:
                    cmd_value = float(cmd_value)
                except ValueError:
                    raise ValueError('Not a float')
            elif cmd_type in VALID_COMMANDS and VALID_COMMANDS[cmd_type] is None:
                cmd_value = None
            # Invalid command
            else:
                raise Exception('Invalid command')

            # Check command value types
            command.type = cmd_type
            command.value = cmd_value
            command.is_new = True
            logg.info('get_latest_command_from_telegram: new command {}:{}'.format(command.type, command.value))
        else:
            raise Exception('Missing ";" in cmd')
