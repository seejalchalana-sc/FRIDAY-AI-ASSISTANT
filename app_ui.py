from flask import Flask, render_template, jsonify, request
import webview
import threading
import shared_state
import random
import time
from main import run_friday, handle_single_command, LOCKED_REJECTION_LINES
from ai_router import split_commands
from face_login import recognize_face
from voice import speak


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status")
def get_status():
    return jsonify({"status": shared_state.current_status})

@app.route("/api/log")
def get_log():
    return jsonify({"log": shared_state.conversation_log})

@app.route("/api/wake")
def api_wake():
    shared_state.trigger_wake = True
    return jsonify({"status": "ok"})

@app.route("/api/is_speaking")
def api_is_speaking():
    return jsonify({"is_speaking": shared_state.is_speaking})

@app.route('/api/text_command', methods=['POST'])
def text_command():
    data = request.get_json()
    user_text = data.get('text', '').strip()

    if not user_text:
        return jsonify({"error": "empty text"}), 400

    shared_state.add_to_log("user", user_text)
    shared_state.set_status("thinking")

    if "check" in user_text:
        success, message = recognize_face()
        if success:
            shared_state.is_unlocked = True
            shared_state.last_face_seen_time = time.time()
            speak("Face recognized. Welcome back, Seejal.")
        else:
            speak(random.choice(LOCKED_REJECTION_LINES))
        shared_state.set_status("idle")
        return jsonify({"status": "ok"})

    if not shared_state.is_unlocked:
        speak(random.choice(LOCKED_REJECTION_LINES))
        shared_state.set_status("idle")
        return jsonify({"status": "ok"})

    sub_commands = split_commands(user_text)
    for sub_command in sub_commands:
        handle_single_command(sub_command)

    shared_state.set_status("idle")

    return jsonify({"status": "ok"})

def start_flask():
    app.run(port=5000)

if __name__ == "__main__":
    flask_thread  = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    friday_thread = threading.Thread(target=run_friday, daemon=True)
    friday_thread.start()

    window = webview.create_window("friday", "http://127.0.0.1:5000", width=900, height=600, frameless=False)
    shared_state.window = window

    webview.start()