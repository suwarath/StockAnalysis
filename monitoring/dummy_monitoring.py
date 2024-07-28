from calendar import Calendar

import requests  # type: ignore

dates = [
    i.strftime("%Y-%m-%d")
    for i in Calendar().itermonthdates(2024, 1)
    if i.month == 1
]

for i in dates:
    ticker_info = {"ticker": "AAPL", "target_date": i}

    url = "http://localhost:9696/get_action"

    response = requests.post(url, json=ticker_info, timeout=60)

    print(response.json())
