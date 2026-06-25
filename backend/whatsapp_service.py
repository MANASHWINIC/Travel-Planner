from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def send_whatsapp_message(destination, trip_plan):

    message = client.messages.create(

        from_=os.getenv("TWILIO_WHATSAPP"),

        to=os.getenv("USER_WHATSAPP"),

        body=f"""
✈️ AI Travel Planner

Destination: {destination}

Your trip itinerary has been generated successfully.

The PDF itinerary is attached.
""",

        media_url=[
    "https://travel-planner-6v9c.onrender.com/download-pdf"
]
    )

    print("Message SID:", message.sid)
    print("Status:", message.status)

    return message.sid