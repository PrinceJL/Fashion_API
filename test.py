import requests

# Define the API endpoint
API_URL = "http://127.0.0.1:8000/recommend"  # Replace with the actual URL if hosted elsewhere

# Define the input payload
payload = {
  "attributes": {
    "fabric_upper": 1,
    "fabric_lower": 2,
    "fabric_outer": 0,
    "pattern_upper": 3,
    "pattern_lower": 2,
    "pattern_outer": 4,
    "sleeve_length": 3,
    "lower_length": 1,
    "socks": 0,
    "hat": 1,
    "glasses": 2,
    "neckwear": 0,
    "wrist_wear": 1,
    "ring": 0,
    "waist_acc": 1,
    "neckline": 0,
    "outer": 1,
    "covers_navel": 1
  },
  "body_shape": "Hourglass",
  "prompt": "I want something comfortable and not too formal for school",
  "top_k": 3,
  "gender": "men"
}

# Send the POST request
response = requests.post(API_URL, json=payload)

# Print the response
if response.status_code == 200:
    print("Top Recommendations:", response.json())
else:
    print("Error:", response.status_code, response.text)