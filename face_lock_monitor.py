import time 
import shared_state
from face_login import check_face_once

CHECK_INTERVAL = 15
LOCK_TIMEOUT = 300

def face_lock_monitor_background():
    while True:
        if shared_state.is_unlocked:
            face_seen = check_face_once()
            if face_seen:
                shared_state.last_face_seen_time = time.time()
            else:
                time_since_seen = time.time() - shared_state.last_face_seen_time
                if time_since_seen > LOCK_TIMEOUT:
                    shared_state.is_unlocked = False
                    print("auto re- locked: face not seen for 5 minutes.")
        time.sleep(CHECK_INTERVAL)