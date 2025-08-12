import requests

url = "http://127.0.0.1:5000/send_voice_alert"

payload = {
    "message": "नमस्ते किसान भाई, आपकी फसल तैयार है।",
    "to": "+919963908010",
    "lang": "hi"  # for Telugu, use "te"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())

