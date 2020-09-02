# Auth
AUTH = {
    "token": "AUTH_SECRET",
    "action": "subscribe",
    "channel": "auth"
}

# Prices
PX_BTC_USD_1M = {
    "action": "subscribe",
    "channel": "prices",
    "symbol": "BTC-USD",
    "granularity": 60
}
PX_BTC_USD_5M = {
    "action": "subscribe",
    "channel": "prices",
    "symbol": "BTC-USD",
    "granularity": 300
}
PX_BTC_USD_1D = {
    "action": "subscribe",
    "channel": "prices",
    "symbol": "BTC-USD",
    "granularity": 86400
}
UN_PX_BTC_USD = {
    "action": "unsubscribe",
    "channel": "prices",
    "symbol": "BTC-USD",
}

# Trades
TRADING = {
    "action": "subscribe", 
    "channel": "trading"
}
UN_TRADING = {
    "action": "unsubscribe", 
    "channel": "trading"
}

# Balance
BALANCES = {
    "action": "subscribe", 
    "channel": "balances"
}
