import requests

from calendar import Calendar
import datetime as dt

dates = [i.strftime('%Y-%m-%d') for i in Calendar().itermonthdates(2024,4) if i.month == 4]

for i in dates:
    ticker_info = {
      'ticker': 'AAPL',
      'target_date': i
    }

    url = 'http://localhost:9696/get_action'

    response = requests.post(url, json = ticker_info)

    print(response.json())