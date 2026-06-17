import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TRAVELPAYOUTS_TOKEN")

AIRLINES = {
    "6E": "IndiGo",
    "AI": "Air India",
    "SG": "SpiceJet",
    "QP": "Akasa Air"
}

def get_flights(origin, destination, travel_date):

    url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"

    headers = {
        "X-Access-Token": TOKEN
    }

    params = {
        "origin": origin,
        "destination": destination,
        "currency": "inr",
        "sorting": "price",
        "limit": 50
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:
        print("Flight API Error:", e)
        return []

    flights = []

    if data.get("success"):

        for item in data.get("data", []):

            flights.append({
                "airline": AIRLINES.get(
                    item.get("airline"),
                    item.get("airline")
                ),
                "price": item.get("price"),
                "duration": item.get("duration"),
                "departure": item.get("departure_at"),
                "gate": item.get("gate"),
                "booking_url":
                    "https://www.aviasales.com" +
                    item.get("link", "")
            })
    print("Flights found:", len(flights))
    # print(flights)
    print("Origin:", origin)
    print("Destination:", destination)
    print("Date:", travel_date)
    #print("Raw API Response:", data)

    return flights