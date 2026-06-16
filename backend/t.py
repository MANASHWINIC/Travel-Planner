from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("YOUR_GROQ_KEY")
print("KEY FOUND:", key[:10] if key else "NONE")

client = Groq(api_key=key)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)