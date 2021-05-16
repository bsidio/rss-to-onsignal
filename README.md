

# Onesignal Push notifications generator.

## Getting Started
### Prerequisites
Here is a list of Python dependencies we're using right now:

* [psycopg2-binary](https://pypi.python.org/pypi/psycopg2-binary)
* [requests](http://docs.python-requests.org/en/master/)
* [feedparser](https://pypi.python.org/pypi/feedparser)


## Features
This simple script does the following list of steps:

1. :see_no_evil: Checks the FEED_URL and looks for new news titles
2. :hear_no_evil: Something new? Let's post 'em all!
3. :speak_no_evil: Empty as a donut hole? Oh no! Let's visit later

## Variables

|Environmenr Variable|  Value|
|--|--|
| DATABASE_URL | ```postgresql://[user[:password]@][netloc][:port][/dbname]``` |
| FEED_URL| URL Link to feed|
|ONESIGNAL_APP_ID| > Requires your OneSignal App's  **REST API Key**, available in  [Keys & IDs](https://documentation.onesignal.com/docs/accounts-and-keys).|
|ONESIGNAL_AUTHORIZATION| > Requires your OneSignal App's  **REST API Key**, available in  [Keys & IDs](https://documentation.onesignal.com/docs/accounts-and-keys).|