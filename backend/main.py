from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
from flight_service import get_flights
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
def get_best_flight(flights):

    if not flights:
        return None

    return min(
        flights,
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

    transport_options = transport_agent(
        data.source,
        data.destination,
        data.travelers,
        data.budget
    )

    origin = AIRPORT_CODES.get(
        data.source,
        "CJB"
    )

    destination = AIRPORT_CODES.get(
        data.destination,
        "GOI"
    )

    flight_data = get_flights(
    origin,
    destination,
    data.travelDate
    )
    recommended_flight = get_best_flight(
    flight_data
    )
    planner_prompt = f"""
    Create a detailed travel itinerary.

    Source: {data.source}
    Destination: {data.destination}
    Travel Date: {data.travelDate}
    Budget: ₹{data.budget}
    Travelers: {data.travelers}
    Duration: {data.days} days
    Preferences: {data.preferences}

    Transport Analysis:
    {transport_options}

    Available Real Flights:
    {flight_data}

    Recommended Flight:
    {recommended_flight}

    Include:

    1. Travel Summary
    2. Recommended Transport
    3. Day-wise Itinerary
    4. Budget Breakdown
    5. Attractions
    6. Travel Tips
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": planner_prompt
            }
        ]
    )

    booking_links = {
        "flights": [
            {
                "name": "MakeMyTrip",
                "url": "https://www.makemytrip.com/flights/"
            },
            {
                "name": "Goibibo Flights",
                "url": "https://www.goibibo.com/flights/"
            },
            {
                "name": "IndiGo",
                "url": "https://www.goindigo.in"
            },
            {
                "name": "Air India",
                "url": "https://www.airindia.com"
            }
        ],
        "hotels": [
            {
                "name": "Booking.com",
                "url": "https://www.booking.com"
            },
            {
                "name": "Agoda",
                "url": "https://www.agoda.com"
            },
            {
                "name": "Goibibo Hotels",
                "url": "https://www.goibibo.com/hotels/"
            }
        ],
        "activities": [
            {
                "name": "Viator",
                "url": "https://www.viator.com"
            },
            {
                "name": "GetYourGuide",
                "url": "https://www.getyourguide.com"
            }
        ]
    }

    return {
    "transport_options": transport_options,
    "flight_data": flight_data,
    "recommended_flight": recommended_flight,
    "trip_plan": response.choices[0].message.content,
    "booking_links": booking_links
}