import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")

def get_trains(
    from_station,
    to_station,
    journey_date
):

    url = "https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations"

    querystring = {
        "fromStationCode": from_station,
        "toStationCode": to_station,
        "dateOfJourney": journey_date
    }

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            params=querystring,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        # print("Train API Response:")
        #print(data)

    except Exception as e:

        print("Train API Error:", e)
        return []

    trains = []

    if data.get("status"):

        for train in data.get("data", [])[:10]:

            trains.append({
            "train_number": train["train_number"],
            "train_name": train["train_name"],
            "from_std": train["from_std"],
            "to_std": train["to_std"],
            "duration": train["duration"],
            "train_type": train["train_type"],
            "class_type": train["class_type"]
            })     

    print("Trains found:", len(trains))
    print("From:", from_station)
    print("To:", to_station)
    print("Date:", journey_date)
    #print("Train API Response:")
    #print(data)

    return trains