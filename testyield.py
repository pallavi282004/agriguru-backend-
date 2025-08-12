import requests

url = "http://127.0.0.1:5000/api/yield"

payload = {
    "crop": "Rice",
    "rainfall": 200,
    "temperature": 30,
    "region": "Andhra Pradesh"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)

try:
    print("Response JSON:", response.json())
except Exception as e:
    print("Error parsing JSON:", e)
    print("Raw Response Text:", response.text)
