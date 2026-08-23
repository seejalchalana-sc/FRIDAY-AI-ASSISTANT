import speech_recognition as sr
import pyttsx3
import pythoncom
import shared_state

def speak(text):
    shared_state.is_speaking = True
    shared_state.set_status("speaking")
    shared_state.add_to_log("friday", text)
    print(f'Friday: {text}')
    try:
        pythoncom.CoInitialize()
        local_engine = pyttsx3.init()
        local_engine.setProperty('rate', 175)
        local_engine.say(text)
        local_engine.runAndWait()
        local_engine.stop()
        del local_engine
    except Exception as e:
        print(f"Error occurred while speaking: {e}")
    shared_state.is_speaking = False

def listen():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 3.5
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration = 0.5)
        audio = recognizer.listen(source, phrase_time_limit=15) 

    try:
        text= recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, didn't catch that.")
        return ""


def listen_for_wake_word():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration = 0.3)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            text = recognizer.recognize_google(audio).lower()
            print(f"Heard: {text}")
            if "friday" in text:
                remaining = text.replace("friday", "", 1).strip()
                return True, remaining
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            pass
        except Exception as e:
            print(f"wake word error: {e}")
    return False, ""
