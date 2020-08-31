# Simple python websocket client
# https://github.com/websocket-client/websocket-client

import websockets
import signal
import sys
import asyncio
import msg
import json
import functools
from logger import get_logger

logg = get_logger('ws_trade')

loop = asyncio.get_event_loop()


class Client():
    def __init__(self):
        self.ws = None

    # Decorator
    def log_sup():
        def wraper(func):
            @functools.wraps(func)
            async def wraped(self):
                await func(self)
                while True:
                    # Wait for at most 20 second
                    try:
                        result = await asyncio.wait_for(self.ws.recv(), timeout=20.0)
                        logg.info("{func} - res: {result}".format(func=func.__name__, result=result))
                    except asyncio.TimeoutError:
                        logg.debug('{func} - timeout!'.format(func=func.__name__))
                        await self.ws.close()
                        break
                    except Exception as e:
                        logg.error('{func} - {error_msg}'.format(func=func.__name__, error_msg=e.args))
                        await self.ws.close()
                        break

            return wraped
        return wraper

    @log_sup()
    async def get_trading_info(self):
        await self.get_auth()
        tr_msg = msg.TRADING
        await self.ws.send(json.dumps(tr_msg))

    @log_sup()
    async def get_price_info(self):
        await self.get_auth()
        px_msg = msg.PX_BTC_USD_60
        await self.ws.send(json.dumps(px_msg))

    async def get_auth(self):
        if self.ws is None:
            logg.info('Get authenticated client')
            url = "wss://ws.prod.blockchain.info/mercury-gateway/v1/ws"
            origin = 'https://exchange.blockchain.com'
            file = open("/home/hungdong/Workspace/secret.exchange.bc")
            key = file.read()
            file.close()

            self.ws = await websockets.connect(uri=url, origin=origin)
            au_msg = msg.AUTH
            au_msg["token"] = key

            await self.ws.send(json.dumps(au_msg))
            result =  await self.ws.recv()

            logg.info(result)


def main():
    trading_cli = Client()
    price_cli = Client()

    tasks = asyncio.gather(
        trading_cli.get_trading_info(),
        # price_cli.get_price_info()
    )

    try:
        loop.run_until_complete(tasks)
    except KeyboardInterrupt as e:
        logg.debug("Caught keyboard interrupt..")
        tasks.cancel()
        loop.run_forever()
        tasks.exception()
    finally:
        loop.close()

if __name__ == "__main__":
    main()