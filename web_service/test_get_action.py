import requests

ticker_info = {"ticker": "AAPL", "target_date": "2024-03-29"}

url = "http://localhost:9696/get_action"

response = requests.post(url, json=ticker_info, timeout=60)

print(response.json())
