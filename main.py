import shared_state
import os
import json
import re
import traceback
import threading
import webview
import time
import random
from datetime import datetime, timedelta
from utils import extract_number, extract_category
from voice import speak, listen, listen_for_wake_word
from brain import ask_friday
from system_control import set_volume, change_volume, set_brightness, change_brightness
from apps import open_app, close_app
from web_actions import search_google, play_youtube, get_date, get_time, get_weather
from notes import add_note, read_notes, delete_all_notes
from expenses import load_expenses, save_expenses, add_expense, get_total_expenses
from reminders import add_reminder, check_due_reminders, reminder_checker_background
from system_info import get_battery_status, get_ram_usage
from ai_router import route_command, split_commands
from screen_vision import describe_screen
from daily_briefing import get_daily_briefing
from face_login import recognize_face
from face_lock_monitor import face_lock_monitor_background

def wrapper_get_weather_info(city):
    return get_weather(city)
def wrapper_get_time_info():
    return get_time()
def wrapper_open_application(app_name):
    success = open_app(app_name.lower())
    if success:
        return f"opening {app_name}"
    return f"sorry, i couldn't open {app_name}"
def wrapper_set_volume(level):
    set_volume(level)
    return f"volume set to {level} percent"
def wrapper_change_volume(direction):
    change_volume(direction)
    return f"volume {'increased' if direction == 'up' else 'decreased'}"
def wrapper_take_note(text):
    add_note(text)
    return "got it, I've noted that down"
def wrapper_close_application(app_name):
    success = close_app(app_name.lower())
    if success:
        return f"closing {app_name}"
    return f"sorry, i couldn't close {app_name}"
AVAILABLE_FUNCTIONS = {
    "get_weather_info": wrapper_get_weather_info,
    "get_time_info": wrapper_get_time_info,
    "open_application": wrapper_open_application,
    "close_application": wrapper_close_application,
    "set_volume": wrapper_set_volume,
    "change_volume": wrapper_change_volume,
    "take_note": wrapper_take_note,
}

LOCKED_REJECTION_LINES = [
    "Wait... where's my boss?",
    "You're not my master. Nice try though.",
    "Access denied. Who even are you?",
    "I don't recognize you. Bold of you to assume I'd just listen.",
    "Hard pass. I only take orders from one person.",
    "Sorry, do I know you?",
]
#Main Loop

   # change_volume("up")  # temporary test

def handle_single_command(command):
    if "daily briefing" not in command and "good morning" not in command and "morning briefing " not in command:
        result = route_command(command, AVAILABLE_FUNCTIONS)
        if result:
            speak(result)
            return

    if "set volume to" in command or "volume to" in command:
        level = extract_number(command)
        if level is not None:
            level = max(0, min(level, 100))
            set_volume(level)
            speak(f"Volume set to {level} percent")
        else:
            speak("sorry, i didn't catch the volume level.")
    elif "volume up" in command:
        change_volume("up")
        speak("volume increased")
    elif "volume down" in command:
        change_volume("down")
        speak("volume decreased")

    elif "set brightness to" in command or "brightness to" in command:
        level = extract_number(command)
        if level is not None:
            level = max(0, min(level, 100))
            set_brightness(level)
            speak(f"brightness set to {level} percent")
        else:
            speak("sorry, i didn't catch the brightness level.")
    elif "brightness up" in command:
        change_brightness("up")
        speak("brightness increased")
    elif "brightness down" in command:
        change_brightness("down")
        speak("brightness decreased")

    elif "open" in command:
        app_found = False
        for app_name in ["notepad", "calculator", "chrome", "vs code", "paint", "file explorer", "word", "excel", "powerpoint", "task manager", "control panel", "settings", "cmd", "command prompt", "spotify", "edge", "firefox"]:
            if app_name in command:
                success = open_app(app_name)
                if success:
                    speak(f"opening {app_name}")
                else:
                    speak(f"sorry, i couldn't open {app_name}")
                app_found = True
                break
        if not app_found:
            speak("sorry, i don't know the app yet.")

    elif "close" in command:
        app_found = False
        for app_name in ["notepad", "calculator", "chrome", "vs code", "paint", "word", "excel", "spotify", "edge", "firefox"]:
            if app_name in command:
                if app_name in command:
                    app_found = True
                    success = close_app(app_name)
                    if success:
                        speak(f"closing {app_name}")
                    else:
                        speak(f"sorry, i couldn't close {app_name}")
                    break
        if not app_found:
            speak("sorry, i don't know the app.")

    elif "search" in command:
        query = command.replace("search google for", "").replace("search for", "").replace("search", "").strip()
        if query:
            search_google(query)
            speak(f"searching google for {query}")
        else:
            speak("what should i search for?")

    elif "play" in command:
        query = command.replace("play", "").replace("on youtube", "").strip()
        if query:
            play_youtube(query)
            speak(f"Playing {query} on youtube")
        else:
            speak("what should i play?")

    elif  "time" in command:
        current_time = get_time()
        speak(f"It's {current_time}")

    elif "what date" in command or "today's date" in command or "what day" in command:
        current_date = get_date()
        speak(f"Today is {current_date}")

    elif "weather" in command:
        city = command.replace("tell me", "").replace("weather in", "").replace("weather for", "").replace("what's the weather", "").replace("weather", "").strip()
        if not city:
            city = "sri ganganagar"
        weather_info = get_weather(city)
        speak(weather_info)

    elif "take a note" in command or "remember that" in command or "add a note" in command:
        note_text = command.replace("take a note", "").replace("remember that", "").replace("add a note", "").strip()
        if note_text:
            add_note(note_text)
            speak("Got it, I've noted that down")
        else:
            speak("What should I note down?")

    elif "read my notes" in command or "what are my notes" in command:
        notes_summary = read_notes()
        speak(notes_summary)

    elif "delete all notes" in command or "clear my notes" in command:
        delete_all_notes()
        speak("All notes deleted")

    elif "how much did i spend today" in command or "today's expenses" in command:
        result = get_total_expenses("today")
        speak(result)

    elif "how much did i spend this month" in command or "this month's expenses" in command:
        result = get_total_expenses("month")
        speak(result)

    elif "total expenses" in command or "how much have i spent" in command:
        result = get_total_expenses("all")
        speak(result)

    elif "spent" in command or "spend" in command or "log expense" in command:
        amount = extract_number(command)
        category = extract_category(command)
        if amount is not None:
            add_expense(amount, category)
            speak(f"Logged {amount} rupees under {category}")
        else:
            speak("How much did you spend?")

    elif "remind me " in command:
        minutes = extract_number(command)
        new_reminder_text = command.split("to", 1)[-1].strip() if "to" in command else command
        if minutes is not None:
            remind_at = add_reminder(new_reminder_text, minutes)
            speak(f"okay, i'll remind you at {remind_at}")
        else:
            speak("in how many minutes should I remind you?")

    elif "battery" in command:
        status = get_battery_status()
        speak(status)

    elif "ram" in command or "memory usage" in command:
        status = get_ram_usage()
        speak(status)

    elif "what is on my screen" in command or "whats on my screen" in command or "what do you see" in command or "take a screenshot" in command or "describe my screen" in command:
        speak("Let me take a look...")
        description = describe_screen()
        speak(description)
    elif "good morning" in command or "daily briefing" in command or "morning briefing" in command:
        briefing = get_daily_briefing()
        speak(briefing)
    else:
        reply = ask_friday(command)
        speak(reply)

def run_friday():
        reminder_thread = threading.Thread(target=reminder_checker_background, daemon=True)
        reminder_thread.start()
        lock_monitor_thread = threading.Thread(target=face_lock_monitor_background, daemon=True)
        lock_monitor_thread.start()
        speak("Friday online. Say 'Friday' to wake me up.")
        while True:
            try:
                shared_state.set_status("idle")

                if shared_state.trigger_wake:
                    shared_state.trigger_wake = False
                    wake_detected = True
                    reminder_text = None
                else:
                    wake_detected, reminder_text = listen_for_wake_word()
                

                if wake_detected:
                    shared_state.set_status("listening")
                    if reminder_text:
                        speak("yes?")
                        command = reminder_text
                    else:
                        speak("yes?")
                        command = listen()
                    
                    shared_state.add_to_log("user", command)

                    if "stop" in command or "exit" in command or "quit" in command:
                        speak("Shutting down. Goodbye!")
                        shared_state.set_status("idle")
                        if shared_state.window:
                            shared_state.window.destroy()
                        break
                    elif command:
                        shared_state.set_status("thinking")

                        if "check" in command:
                            speak("Let me take a look...")
                            success, message = recognize_face()
                            if success:
                                shared_state.is_unlocked = True
                                shared_state.last_face_seen_time = time.time()
                                speak("Face recognized. Welcome back, Seejal.")
                            else:
                                speak(random.choice(LOCKED_REJECTION_LINES))
                        elif not shared_state.is_unlocked:
                            speak(random.choice(LOCKED_REJECTION_LINES))
                        else:
                            sub_commands = split_commands(command)
                            for sub_command in sub_commands:
                                handle_single_command(sub_command)
                        
            except Exception as e:
                print(f'main loop error: "{e}')

                        

if __name__ == "__main__":
    run_friday()