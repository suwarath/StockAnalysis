import requests

ticker_info = {
  'ticker': 'AAPL',
  'target_date': '2024-01-05'
}

url = 'http://localhost:9696/get_action'

response = requests.post(url, json = ticker_info)

print(response.json())