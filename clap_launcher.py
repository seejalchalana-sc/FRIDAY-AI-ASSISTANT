import pyaudio
import numpy as np
import psutil
import subprocess
import requests
import time

CHUNK = 1024
RATE = 44100
CLAP_THRESHOLD = 150
TRIPLE_CLAP_WINDOW = 2.0
COOLDOWN_AFTER_ACTION = 1.5
DECISION_WAIT = 0.6
last_speaking_check = 0
friday_is_speaking = False
SPEAKING_CHECK_INTERVAL = 0.2

FRIDAY_EXE_PATH = r"D:\jarvis final\dist\Friday.exe"
FRIDAY_PROCESS_NAME = "Friday.exe"


def is_friday_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == FRIDAY_PROCESS_NAME:
            return True
    return False


def launch_friday():
    print("launching friday...")
    subprocess.Popen([FRIDAY_EXE_PATH])


def close_friday():
    print("closing friday...")
    subprocess.run(["taskkill", "/IM", FRIDAY_PROCESS_NAME, "/F"])


def wake_friday():
    print("waking friday...")
    try:
        requests.get("http://127.0.0.1:5000/api/wake", timeout=2)
    except requests.exceptions.RequestException as e:
        print(f"couldn't reach friday's server: {e}")

def check_if_speaking():
    global last_speaking_check, friday_is_speaking
    now = time.time()
    if now - last_speaking_check > SPEAKING_CHECK_INTERVAL:
        last_speaking_check = now
        try:
            resp = requests.get("http://127.0.0.1:5000/api/is_speaking", timeout=0.5)
            friday_is_speaking = resp.json().get("is_speaking", False)
        except requests.exceptions.RequestException:
            friday_is_speaking = False  # Friday probably isn't running, assume not speaking
    return friday_is_speaking

def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=RATE,
                     input=True,
                     frames_per_buffer=CHUNK)

    print("clap launcher running. listening for claps...")

    clap_times = []
    last_clap_time = 0

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(audio_data).mean()
            
            now = time.time()

            if volume > CLAP_THRESHOLD and (now - last_clap_time) > 0.3 and not check_if_speaking():
                clap_times.append(now)
                last_clap_time = now
                clap_times = [t for t in clap_times if now - t <= TRIPLE_CLAP_WINDOW]
                print(f"clap registered, count in window: {len(clap_times)}")

            if clap_times and (now - clap_times[-1]) > DECISION_WAIT:
                if len(clap_times) >= 3:
                    print("triple clap detected")
                    if is_friday_running():
                        close_friday()
                    clap_times = []
                    time.sleep(COOLDOWN_AFTER_ACTION)

                elif len(clap_times) == 1:
                    print("single clap detected")
                    if is_friday_running():
                        wake_friday()
                    else:
                        launch_friday()
                    clap_times = []
                    time.sleep(COOLDOWN_AFTER_ACTION)

                else:
                    clap_times = []

    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("clap launcher stopped.")


if __name__ == "__main__":
    main()