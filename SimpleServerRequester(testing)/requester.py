import requests

url = 'http://127.0.0.1:5000/get_link'  # Update the URL to include the route

username = 'chris_benjamin'
lounge_id = 'lg_3124'
from_date = '11/11/2023 16:00'
to_date = '11/11/2023 20:00'

price = 1200
item = 'YYZ International Lounge'
currency = 'usd'

# Define the payload as a dictionary
payload = {
    'username': username,
    'lounge_id': lounge_id,
    'from_date': from_date,
    'to_date': to_date,
    'price': price,
    'item': item,
    'currency': currency
}

# Send a POST request with JSON payload
response = requests.post(url, json=payload)  # Use json instead of data

# Check the response
if response.status_code == 200:
    print("Request was successful.")
    print("Response Data:", response.json())
else:
    print("Request failed with status code:", response.status_code)
