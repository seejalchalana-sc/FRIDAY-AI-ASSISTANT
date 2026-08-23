import pyaudio
import numpy as np
import time

CHUNK = 1024
RATE = 44100
CLAP_THRESHOLD = 3000
COOLDOWN = 1.0

def listen_for_clap():
    """
    Blocks until a clap-like sound is detected.
    retuns Tue once a clap is heard.
    """
    p= pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("listening for clap...")
    try:
        while True:
            data =  stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(audio_data).mean()

            if volume > CLAP_THRESHOLD:
                print(f"clap detected! volume:{volume}")
                stream.stop_stream()
                stream.close()
                p.terminate()
                return True
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()
        return False