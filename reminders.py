import json 
import os
from datetime import datetime, timedelta
from voice import speak
import time


REMINDERS_FILE = "reminders.json"
def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)


def add_reminder(text, minutes_from_now):
    reminders = load_reminders()
    remind_time = datetime.now() + timedelta(minutes=minutes_from_now)
    reminders.append({
        "text": text,
        "remind_at": remind_time.strftime("%Y-%m-%d %H:%M:%S"),
        "done": False
    }) 
    save_reminders(reminders)
    return remind_time.strftime("%I:%M %p")

def check_due_reminders():
    reminders = load_reminders()
    now = datetime.now()
    due = []
    updated = False

    for r in reminders:
        if not r["done"]:
            remind_time = datetime.strptime(r["remind_at"], "%Y-%m-%d %H:%M:%S")
            if now >= remind_time:
                due.append(r["text"])
                r["done"] = True
                updated = True

    if updated:
        save_reminders(reminders)

    return due

def reminder_checker_background():
    while True:
        due_reminders = check_due_reminders()
        for reminder_text in due_reminders:
            speak(f"Reminder: {reminder_text}")
        time.sleep(5)

