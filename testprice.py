import requests

url = "http://127.0.0.1:5000/api/price"
payload = {
    "crop": "Wheat",
    "region": "North"
}

response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
