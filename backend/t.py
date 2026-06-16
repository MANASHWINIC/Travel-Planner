import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TRAVELPAYOUTS_TOKEN")

headers = {
    "X-Access-Token": TOKEN
}

url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"

params = {
    "origin": "MAA",
    "destination": "DEL",
    "departure_at": "2026-07"
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

print(response.status_code)
print(response.text[:1000])