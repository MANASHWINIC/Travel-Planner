from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import travel_graph as tg
from fastapi.responses import FileResponse
from fastapi import HTTPException
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
class ApprovalRequest(BaseModel):
    trip_data: dict
class ReplanRequest(BaseModel):

    trip_data: dict

    feedback: str
@app.post("/approve-trip")
def approve_trip(request: ApprovalRequest):

    state = request.trip_data

    state = tg.execution_agent(state)

    return {
        "message": "Execution completed successfully.",

        "pdf_path": state.get("pdf_path"),

        "calendar_status": state.get("calendar_status"),

        "whatsapp_status": state.get("whatsapp_status")
    }
@app.post("/replan-trip")
def replan_trip(request: ReplanRequest):

    state = request.trip_data

    state["feedback"] = request.feedback

    state = tg.replanning_agent(state)

    return {

        "message": "Trip replanned successfully.",

        "trip_plan": state["trip_plan"],

        "trip_data": state
    }


@app.get("/")
def home():
    return {
        "message": "Travel Planner API Running"
    }
@app.get("/download-pdf")
def download_pdf():

    pdf_path = "Trip_Itinerary.pdf"

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404,
            detail="PDF not found"
        )

    return FileResponse(
        path=pdf_path,
        filename="Trip_Itinerary.pdf",
        media_type="application/pdf"
    )

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

    result = tg.graph.invoke({
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

    "recommended_flight": get_best_flight(result["flights"]),

    "train_data": result["trains"],

    "recommended_train": get_best_train(result["trains"]),

    "hotel_data": result["hotels"],

    "recommended_hotel": get_best_hotel(result["hotels"]),

    "trip_plan": result["trip_plan"],

    # Entire state returned for approval
    "trip_data": result
}