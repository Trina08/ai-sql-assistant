import requests
import json

url = "http://127.0.0.1:8000/ask"

payload = {"question": "Show me all products and their prices"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("❌ Error sending request:", e)
