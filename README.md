# This project APIs to get notifications from and send alert to Telegram bot

## Prerequisites

```bash
git clone https://github.com/nopp/alertmanager-webhook-telegram-go.git
patch -p1 < patches/get-noti-from-telegram.patch
sed -i s/xxbotTokenxx/"$bottoken"/ alert/alert.go
sed -i s/666777666/"$chatid"/ alert/alert.go

go clean && go build && ./alertmanager-webhook-telegram-go
```

## Run

`./run_forever.py --py main.py --go alertmanager-webhook-telegram-go`

## Telegram commands

ls; # List available commands 
get_info; # Get info about btc reference point, price change offset, alert trigger, etc. 
update_ref;<value>
update_offset;<value>
alert_at;<value>

cont_ref; # Continue notification
cont_alert; # Continue alerting

get_price_5m; # Get latest price block in 5-min period
get_price_1d; # Get latest price block in 1-day period