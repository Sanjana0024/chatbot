import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print("API Key Loaded:", api_key)
print("Creating Groq client")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print("created successfully")

def generate_reply(history):

    messages = []

    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": str(msg["content"])
        })

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    return chat.choices[0].message.content