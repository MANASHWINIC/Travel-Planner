from typing import TypedDict
from langgraph.graph import StateGraph, END
from flight_service import get_flights
from train_service import get_trains
from hotel_service import get_hotels
from datetime import datetime, timedelta
from groq import Groq
from dotenv import load_dotenv
import os

# ------------------------------
# Session Storage
# ------------------------------


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

    # User Input
    source: str
    destination: str
    budget: int
    travelers: int
    days: int
    travelDate: str
    preferences: str

    # API Results
    flights: list
    trains: list
    hotels: list

    # Agent Results
    trip_plan: str

    # Approval
    approved: bool
    feedback: str

    # Execution
    pdf_path: str
    whatsapp_status: str

    


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
# Planner Agent
# --------------------

def planner_agent(state):

    prompt = f"""
You are an autonomous AI Travel Planning Agent.

Your responsibilities are:

1. Compare all available flights.
2. Compare all available trains.
3. Compare all available hotels.
4. Consider:

- Budget
- Travel duration
- Comfort
- Number of stops
- Hotel ratings
- Hotel price
- User preferences

Do NOT always choose the cheapest option.

Reason carefully and choose the BEST overall travel plan.

Explain WHY you selected the transport and hotel.

User Details

Source:
{state["source"]}

Destination:
{state["destination"]}

Budget:
₹{state["budget"]}

Travelers:
{state["travelers"]}

Days:
{state["days"]}

Preferences:
{state["preferences"]}

Flights

{state["flights"]}

Trains

{state["trains"]}

Hotels

{state["hotels"]}

Generate:

1. Travel Summary

2. Recommended Transport
(Explain why.)

3. Recommended Hotel
(Explain why.)

4. Complete Day-wise Itinerary

5. Budget Breakdown

6. Attractions

7. Food Recommendations

8. Travel Tips

Think step-by-step before making your recommendation.
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
def replanning_agent(state):

    print("========== REPLANNING AGENT ==========")

    prompt = f"""
You are an intelligent travel replanning agent.

The user was NOT satisfied with the current itinerary.

Current itinerary:

{state["trip_plan"]}

User feedback:

{state["feedback"]}

Modify ONLY the parts related to the feedback.

Examples:

- If user asks for cheaper hotel:
    Change hotel only.

- If user wants morning flight:
    Change flight only.

- If user wants more sightseeing:
    Add attractions only.

Keep everything else unchanged.

Return the updated itinerary.
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

    state["trip_plan"] = response.choices[0].message.content

    print("Replanning Agent Completed")

    return state
def execution_agent(state):

    print("========== EXECUTION AGENT ==========")

    state = pdf_agent(state)
    try:
        state = whatsapp_agent(state)
        state["whatsapp_status"] = "Sent successfully"
    except Exception as e:
        print("WhatsApp Error:", e)
        state["whatsapp_status"] = f"Failed: {e}"

    print("Execution Agent Completed")

    return state
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import darkblue
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle


def pdf_agent(state):

    filename = "Trip_Itinerary.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
    "Title",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    textColor=darkblue,
    spaceAfter=10,
    spaceBefore=0
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        spaceBefore=6,
        spaceAfter=4
    )

    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["BodyText"],
        leading=16,
        spaceBefore=0,
        spaceAfter=2
    )

    story = []

    # Title
    story.append(
        Paragraph(
            "AI Travel Planner",
            title_style
        )
    )

    story.append(
        Spacer(1, 3)
    )

    # Trip Summary
    story.append(
        Paragraph(
            "<b>Trip Summary</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"""
            <b>Source:</b> {state["source"]}<br/>
            <b>Destination:</b> {state["destination"]}<br/>
            <b>Travel Date:</b> {state["travelDate"]}<br/>
            <b>Duration:</b> {state["days"]} Days<br/>
            <b>Budget:</b> ₹{state["budget"]}<br/>
            <b>Travellers:</b> {state["travelers"]}<br/>
            """,
            normal_style
        )
    )

    story.append(
        Spacer(1, 3)
    )

    # Itinerary
    story.append(
        Paragraph(
            "<b>Travel Itinerary</b>",
            heading_style
        )
    )

    itinerary = state["trip_plan"]

    # Preserve line breaks
    for line in itinerary.split("\n"):

        line = line.strip()

        if line == "":
            if line == "":
                story.append(Spacer(1, 2))
        else:
            story.append(
                Paragraph(
                    line.replace(
                        "&", "&amp;"
                    ),
                    normal_style
                )
            )

    doc.build(story)

    state["pdf_path"] = filename

    print("PDF Generated Successfully")

    return state
from whatsapp_service import send_whatsapp_message


def whatsapp_agent(state):

    print("========== WHATSAPP AGENT ==========")

    try:

        send_whatsapp_message(state)

        state["whatsapp_status"] = "Sent Successfully"

    except Exception as e:

        print("WhatsApp Error:", e)

        state["whatsapp_status"] = str(e)

    print("WhatsApp Agent Completed")

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