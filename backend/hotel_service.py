import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPID_API_KEY = os.getenv("RAPIDAPI_KEY")

HEADERS = {
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": "booking-com15.p.rapidapi.com"
}


def get_hotels(city, checkin, checkout):

    try:

        # STEP 1: Get destination id

        destination_url = (
            "https://booking-com15.p.rapidapi.com/"
            "api/v1/hotels/searchDestination"
        )

        destination_response = requests.get(
            destination_url,
            headers=HEADERS,
            params={"query": city}
        )

        destination_data = destination_response.json()
        #print(destination_data)

        if not destination_data["data"]:
            return []

        destination = None

        for item in destination_data["data"]:
            if item.get("country") == "India":
                destination = item
                break

        if destination is None:
            destination = destination_data["data"][0]

        dest_id = destination["dest_id"]
        search_type = destination["search_type"]

        print("Selected:", destination["name"])
        print("Country:", destination["country"])
        print("Destination ID:", dest_id)
        print("Search Type:", search_type)

        # STEP 2: Search hotels

        hotel_url = (
            "https://booking-com15.p.rapidapi.com/"
            "api/v1/hotels/searchHotels"
        )

        params = {
            "dest_id": dest_id,
            "search_type": search_type.upper(),
            "arrival_date": checkin,
            "departure_date": checkout,
            "adults": "2",
            "room_qty": "1",
            "page_number": "1",
            "currency_code": "INR"
        }

        hotel_response = requests.get(
            hotel_url,
            headers=HEADERS,
            params=params
        )

        hotel_data = hotel_response.json()
        #print("Hotel API Response:")
        #print(hotel_data)
        hotel_data["data"]["hotels"]
        #print(hotel_data.keys())
        #print(hotel_data.get("data"))
        hotels = []

        for hotel in hotel_data.get("data", {}).get(
            "hotels", []
        )[:10]:

            property_data = hotel.get(
                "property", {}
            )

            hotel_name = property_data.get("name", "")

            hotels.append({
                "name": hotel_name,

                "rating":
                    property_data.get(
                        "reviewScore"
                    ),

                "address":
                    property_data.get(
                        "wishlistName"
                    ),

                "price":
                    property_data.get(
                        "priceBreakdown", {}
                    ).get(
                        "grossPrice", {}
                    ).get(
                        "value"
                    ),

                "currency":
                    property_data.get(
                        "currency"
                    ),

                "booking_url":
                    f"https://www.booking.com/searchresults.html?ss={hotel_name}",

                "agoda_url":
                    f"https://www.agoda.com/search?text={hotel_name}",

                "goibibo_url":
                    "https://www.goibibo.com/hotels/",

                "makemytrip_url":
                    "https://www.makemytrip.com/hotels/"
            })
                   

        print(
            f"Hotels found: {len(hotels)}"
        )

        return hotels

    except Exception as e:

        print(
            "Hotel API Error:",
            e
        )

        return []