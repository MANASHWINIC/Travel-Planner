from typing import TypedDict
from langgraph.graph import StateGraph, END
from flight_service import get_flights
from train_service import get_trains
from hotel_service import get_hotels
from datetime import datetime, timedelta
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
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


class TravelState(TypedDict):

    source: str
    destination: str
    budget: int
    travelers: int
    days: int
    travelDate: str
    preferences: str

    flights: list
    trains: list
    hotels: list

    trip_plan: str

    


# --------------------
# Flight Agent
# --------------------

def flight_agent(state):

    origin = AIRPORT_CODES.get(
        state["source"],
        "CJB"
    )

    destination = AIRPORT_CODES.get(
        state["destination"],
        "GOI"
    )

    state["flights"] = get_flights(
        origin,
        destination,
        state["travelDate"]
    )

    print("Flight Agent Completed")

    return state


# --------------------
# Train Agent
# --------------------

def train_agent(state):

    source_station = STATION_CODES.get(
        state["source"]
    )

    destination_station = STATION_CODES.get(
        state["destination"]
    )

    if source_station and destination_station:

        journey_date = datetime.strptime(
            state["travelDate"],
            "%Y-%m-%d"
        ).strftime("%d-%m-%Y")

        state["trains"] = get_trains(
            source_station,
            destination_station,
            journey_date
        )

    else:

        state["trains"] = []

    print("Train Agent Completed")

    return state


# --------------------
# Hotel Agent
# --------------------

def hotel_agent(state):

    checkout_date = (
        datetime.strptime(
            state["travelDate"],
            "%Y-%m-%d"
        )
        +
        timedelta(days=state["days"])
    ).strftime("%Y-%m-%d")

    state["hotels"] = get_hotels(
        state["destination"],
        state["travelDate"],
        checkout_date
    )

    print("Hotel Agent Completed")

    return state
# --------------------
# Budget Agent
# --------------------

def budget_agent(state):

    cheapest_flight = 0

    if state["flights"]:

        cheapest_flight = min(
            state["flights"],
            key=lambda x: x["price"]
        )["price"]

    hotel_budget = (
        state["budget"]
        - cheapest_flight * state["travelers"]
    )

    filtered_hotels = []

    for hotel in state["hotels"]:

        if (
            hotel.get("price")
            and hotel["price"] <= hotel_budget
        ):
            filtered_hotels.append(hotel)

    state["hotels"] = filtered_hotels

    print(
        f"Budget Agent: {len(filtered_hotels)} hotels within budget"
    )

    return state


    filtered_hotels = []

    for hotel in state["hotels"]:

        price = hotel.get("price")

        if price and price <= state["budget"]:
            filtered_hotels.append(hotel)

    state["hotels"] = filtered_hotels

    print(
        f"Budget Agent: {len(filtered_hotels)} hotels within budget"
    )

    return state
# --------------------
# Planner Agent
# --------------------

def planner_agent(state):

    prompt = f"""
    Create a detailed travel itinerary.

    Source: {state['source']}
    Destination: {state['destination']}
    Budget: ₹{state['budget']}
    Travelers: {state['travelers']}
    Duration: {state['days']} days
    Preferences: {state['preferences']}

    Available Flights:
    {state['flights']}

    Available Trains:
    {state['trains']}

    Available Hotels:
    {state['hotels']}

    Include:

    1. Travel Summary
    2. Recommended Transport
    3. Recommended Hotel
    4. Day-wise Itinerary
    5. Budget Breakdown
    6. Attractions
    7. Travel Tips
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

    state["trip_plan"] = (
        response.choices[0]
        .message.content
    )

    print("Planner Agent Completed")

    return state

# --------------------
# Build Graph
# --------------------

workflow = StateGraph(
    TravelState
)

workflow.add_node(
    "flight_agent",
    flight_agent
)

workflow.add_node(
    "train_agent",
    train_agent
)

workflow.add_node(
    "hotel_agent",
    hotel_agent
)
workflow.add_node(
    "planner_agent",
    planner_agent
)
workflow.add_node(
    "budget_agent",
    budget_agent
)

workflow.set_entry_point(
    "flight_agent"
)

workflow.add_edge(
    "flight_agent",
    "train_agent"
)

workflow.add_edge(
    "train_agent",
    "hotel_agent"
)

workflow.add_edge(
    "hotel_agent",
    "budget_agent"
)

workflow.add_edge(
    "budget_agent",
    "planner_agent"
)

workflow.add_edge(
    "planner_agent",
    END
)

graph = workflow.compile()



if __name__ == "__main__":

    result = graph.invoke({
        "source": "Chennai",
        "destination": "Goa",
        "budget": 30000,
        "travelers": 2,
        "days": 3,
        "travelDate": "2026-07-15",
        "preferences": "Beach"
    })

    print("\n===== SUMMARY =====")

    print(
        "Flights:",
        len(result["flights"])
    )

    print(
        "Trains:",
        len(result["trains"])
    )

    print(
        "Hotels:",
        len(result["hotels"])
    )

    print("\n===== TRIP PLAN =====")

    print(
        result["trip_plan"]
    )