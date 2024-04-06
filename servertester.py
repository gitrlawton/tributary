import requests as requests

data = {
    "engine_temperature": 0.6,
}

response = requests.post("http://localhost:8000/record", json=data)
print(response.content)