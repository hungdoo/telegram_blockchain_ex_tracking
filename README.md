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

`python main.py`