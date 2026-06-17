from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
from travel_graph import graph
AIRPORT_CODES = {
    "Coimbatore": "CJB",
    "Goa": "GOI",
    "Chennai": "MAA",
    "Bangalore": "BLR",
    "Mumbai": "BOM",
    "Delhi": "DEL",
    "Hyderabad": "HYD",
    "Kochi": "COK",
    "Pune": "PNQ",
    "Kolkata": "CCU",
    "Ahmedabad": "AMD"
}
STATION_CODES = {
    "Chennai": "MAS",
    "Delhi": "NDLS",
    "Mumbai": "CSMT",
    "Bangalore": "SBC",
    "Hyderabad": "SC",
    "Coimbatore": "CBE",
    "Kochi": "ERS",
    "Goa": "MAO",
    "Pune": "PUNE",
    "Kolkata": "HWH",
    "Ahmedabad": "ADI"
}
def get_best_flight(flights):

    if not flights:
        return None

    return min(
        flights,
        key=lambda x: x["price"]
    )
def get_best_train(trains):

    if not trains:
        return None

    return min(
        trains,
        key=lambda x: int(
            x["duration"].split(":")[0]
        )
    )


def get_best_hotel(hotels):

    if not hotels:
        return None

    hotels_with_price = [
        hotel
        for hotel in hotels
        if hotel.get("price")
    ]

    if not hotels_with_price:
        return None

    return min(
        hotels_with_price,
        key=lambda x: x["price"]
    )
# Load environment variables
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripRequest(BaseModel):
    source: str
    destination: str
    budget: int
    travelers: int
    days: int
    travelDate: str
    preferences: str


@app.get("/")
def home():
    return {
        "message": "Travel Planner API Running"
    }


def transport_agent(source, destination, travelers, budget):

    prompt = f"""
    Compare travel options from {source} to {destination}.

    Travelers: {travelers}
    Budget: ₹{budget}

    Give:

    FLIGHT OPTION
    - Estimated Cost
    - Travel Time
    - Pros
    - Cons

    TRAIN OPTION
    - Estimated Cost
    - Travel Time
    - Pros
    - Cons

    BUS OPTION
    - Estimated Cost
    - Travel Time
    - Pros
    - Cons

    Finally recommend the best option.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
@app.post("/generate-trip")
def generate_trip(data: TripRequest):

    result = graph.invoke({
        "source": data.source,
        "destination": data.destination,
        "budget": data.budget,
        "travelers": data.travelers,
        "days": data.days,
        "travelDate": data.travelDate,
        "preferences": data.preferences
    })

    return {
    "flight_data": result["flights"],

    "recommended_flight":
        get_best_flight(result["flights"]),

    "train_data": result["trains"],

    "recommended_train":
        get_best_train(result["trains"]),

    "hotel_data": result["hotels"],

    "recommended_hotel":
        get_best_hotel(result["hotels"]),

    "trip_plan":
        result["trip_plan"]
}