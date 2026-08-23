import webbrowser
from urllib.parse import quote
from datetime import datetime
import requests
import os

def search_google(query):
    encoded_query = quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(url)

def play_youtube(query):
    encoded_query = quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    webbrowser.open(url)

def get_time():
    now = datetime.now()
    return now.strftime("%I:%M %p")

def get_date():
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y")

def get_weather(city="sri ganganagar"):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    encoded_city = quote(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            feels_like = data["main"]["feels_like"]
            return f"It's {temp} degrees celsius in {city}, feels like {feels_like} degrees, with {description}."
        elif response.status_code == 404:
            return f"I couldn't find a city called {city}. Could you try again with the full city name?"
        else:
            return "sorry, I couldn't fetch the weather right now."
    except requests.exceptions.Timeout:
        return "The weather service took too long to respond. Please try again."
    except Exception as e:
        print(f"Weather error: {e}")
        return "sorry, I'm having trouble getting the weather."
