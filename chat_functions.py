import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print("API Key Loaded:", api_key)
print("Creating Groq client")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print("created successfully")

def generate_reply(user_message):
    print("User message received:")
    print(user_message)


    chat = client.chat.completions.create(
        messages=[
            {"role": "user", "content": user_message}
        ],
        model="llama3-8b-8192"
    )
    print("Response received from groq")
    reply = chat.choices[0].message.content

    print("AI Reply:")
    print(reply)

    return reply