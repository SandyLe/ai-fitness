import requests

# Test the root endpoint
response = requests.get("http://localhost:8000/")
print(response.json())

# Test the generate endpoint
response = requests.post(
    "http://localhost:8000/generate",
    json={"prompt": "Hello", "max_new_tokens": 10, "temperature": 0.7}
)
print(response.json())