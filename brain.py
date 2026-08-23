from groq import Groq
from dotenv import load_dotenv
import os
import json
import traceback

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MEMORY_FILE = "conversation_history.json"

def load_history():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return [
        {"role": "system", "content": "You are Friday, a helpful voice assistant. Keep replies short and conversational. When responding in Hindi or Hinglish, write Hindi words using English/Roman letters only (e.g., 'aap kaise ho', not Devanagari script), since your text-to-speech voice can only pronounce English phonetics correctly. Avoid Devanagari script entirely. Never add English translations in brackets after Hindi phrases — just respond naturally in one language or a natural Hinglish mix, without repeating the same meaning twice."}
    ]

def save_history(history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

conversation_history = load_history()

def ask_friday(prompt):
    global conversation_history
    conversation_history.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
           messages=conversation_history
        )
        reply = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": reply})
        save_history(conversation_history)
        return reply
    except Exception as e:
        print(f"Brain error: {e}")
        traceback.print_exc()
        return "Sorry, I'm having trouble thinking right now."


