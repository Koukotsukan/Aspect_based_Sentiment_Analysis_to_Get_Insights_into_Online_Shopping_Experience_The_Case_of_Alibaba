import requests
import json

url = "http://localhost:4999/predict"
data = {"text": "The phone is good, but the service is bad."}
headers = {"Content-type": "application/json", "Accept": "text/plain"}
r = requests.post(url, data=json.dumps(data), headers=headers)
print(r.text)
