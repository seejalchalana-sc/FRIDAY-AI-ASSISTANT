import json 
import os
from datetime import datetime

NOTES_FILE = "notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

def add_note(note_text):
    notes = load_notes()
    notes.append({
        "text": note_text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p")
    })
    save_notes(notes)

def read_notes():
    notes = load_notes()
    if not notes:
        return "You don't have any notes yet."
    notes_list = ", ".join([n["text"] for n in notes])
    return f"You have {len(notes)} notes: {notes_list}"

def delete_all_notes():
    save_notes([])