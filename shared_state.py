current_status = "idle"
conversation_log = []
is_unlocked = False
last_face_seen_time = 0

trigger_wake =  False
is_speaking = False
def set_status(status):
    global current_status
    current_status = status

def add_to_log(role, text):
    conversation_log.append({"role": role, "text": text})