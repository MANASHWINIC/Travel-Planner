from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def send_whatsapp_message(state):

    # Flight
    flight = "Not Available"
    if state.get("flights"):
        cheapest = min(state["flights"], key=lambda x: x["price"])
        flight = (
            f"{cheapest.get('airline', 'Flight')} - "
            f"₹{cheapest.get('price', 'N/A')}"
        )

    # Hotel
    hotel = "Not Available"
    if state.get("hotels"):
        cheapest_hotel = min(
            state["hotels"],
            key=lambda x: x.get("price", 999999)
        )

        hotel = (
            f"{cheapest_hotel.get('name', 'Hotel')} - "
            f"₹{cheapest_hotel.get('price', 'N/A')}/night"
        )

    # Itinerary Summary
    summary = state["trip_plan"][:700]

    message = client.messages.create(

        from_=os.getenv("TWILIO_WHATSAPP"),

        to=os.getenv("USER_WHATSAPP"),

        body=f"""
✈️ *AI Travel Planner*

📍 Destination: {state['destination']}

📅 Travel Date: {state['travelDate']}

🧳 Duration: {state['days']} Days

👤 Travelers: {state['travelers']}

💰 Budget: ₹{state['budget']}

----------------------------

✈️ Recommended Flight

{flight}

----------------------------

🏨 Recommended Hotel

{hotel}

----------------------------

🗺️ Trip Highlights

{summary}

----------------------------

Thank you for using AI Travel Planner ❤️
"""
    )

    print("Message SID:", message.sid)
    print("Status:", message.status)

    return message.sid