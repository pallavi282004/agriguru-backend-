import requests

url = "http://127.0.0.1:5000/api/recommend"

payload = {
    "soil": "Loamy",
    "rainfall": 200,
    "temperature": 27,
    "region": "South"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
