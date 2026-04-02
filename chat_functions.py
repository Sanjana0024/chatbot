
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_reply(history):
    """
    Generate a response from Groq API given the conversation history.

    Parameters:
        history (list of dict): Each dict has keys 'role' and 'content'

    Returns:
        str: AI response text
    """


    response = client.chat.completions.create(
        model="llama3-8b-8192", 
        messages=history
    )

    
    ai_reply = response.choices[0].message.content

    return ai_reply