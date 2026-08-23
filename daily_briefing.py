from brain import client
from web_actions import get_weather, get_date
from reminders import load_reminders
from datetime import datetime

def get_todays_reminders_summary():
    reminders = load_reminders()
    today_str = datetime.now().strftime("%Y=%m-%d")

    today_reminders = [
        r for r in reminders
        if not r["done"] and r["remind_at"].startswith(today_str)
    ]
    count = len(today_reminders)
    if count == 0:
        return "no reminders today"
    return f"{count} reminders{'s' if count !=1 else ''} today"

def get_daily_briefing(city="mohali"):
    date_str = get_date()
    weather_str = get_weather
    reminders_str = get_todays_reminders_summary()

    prompt = (
        f"Combine these facts into one warm, natural-sounding morning briefing, "
        f"like a friendly assistant greeting someone at the start of their day. "
        f"Keep it fairly brief, 2-4 sentences, and end with a short motivational line. "
        f"Don't use bullet points or a list format, just natural flowing speech.\n\n"
        f"Today's date: {date_str}\n"
        f"Weather: {weather_str}\n"
        f"Reminders: {reminders_str}"
    )

    messages = [
        {"role": "system", "content": "You are Friday, a warm and encouraging personal assistant."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )

    return response.choices[0].message.content.strip()