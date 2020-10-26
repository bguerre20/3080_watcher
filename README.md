# 3080_watcher

This is a basic Python web scraper of newegg and best buy to check stock of 3080s

## Requirements

Have the following python modules installed: 
 - requests
 - BeautifulSoup4
 - dotenv
 - twilio

## Configuration

Need to setup your own .env file with the following variables: 

```shell
WATCHER_TWILIO_AUTH_TOKEN=
WATCHER_TWILIO_ACCOUNT_SID=
WATCHER_BBY_KEY=
WATCHER_PHONE_NUMBER=
WATCHER_EMAIL_ADDRESS=
WATCHER_TWILIO_FROM_NUMBER=
```

## Make it a go go
Setup a windows task scheduler to run this code periodically, good luck!
