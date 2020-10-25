3080_watcher
This is a basic Python web scraper of newegg and best buy to check stock of 3080s

0. Need to setup your own .env file with the following variables: 
    WATCHER_TWILIO_AUTH_TOKEN=
    WATCHER_TWILIO_ACCOUNT_SID=
    WATCHER_BBY_KEY=
    WATCHER_PHONE_NUMBER=
    WATCHER_EMAIL_ADDRESS=
    WATCHER_TWILIO_FROM_NUMBER=
1. Have the following modules installed: 
    requests
    BeautifulSoup4
    dotenv
    twilio
    ElementTree
2.  Setup a windows task scheduler to run this code periodically, good luck!
