import requests
import json
from logger import get_logger

logg = get_logger()

# Const
UPDATE_REF = 'update_ref'
ALERT_AT = 'alert_at'
GET_PRICE_5M = 'get_price_5m'
GET_PRICE_1D = 'get_price_1d'
LIST_CMD = 'ls'
CONT_ALERT = 'cont_alert'
CONT_REF = 'cont_ref'
GET_INFO = 'get_info'

VALID_COMMANDS = {
    # Command: value type
    UPDATE_REF: float, # Update reference/target value
    ALERT_AT: float, # Alert at specific price
    CONT_REF: None, # Clear SEEN flag to cont. receiving Change price
    CONT_ALERT: None, # Clear SEEN flag to cont. receiving Alert price
    GET_PRICE_5M: None, # Get current price 5 min
    GET_PRICE_1D: None, # Get current price 1 day
    LIST_CMD: None, # List all avail. commands
    GET_INFO: None, # List all avail. commands
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
            cmd_type, cmd_value = text.lower().split(';')
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
