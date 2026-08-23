from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc


def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume

def set_volume(level):
    #level should be 0 to 100
    volume = get_volume_interface()
    volume.SetMasterVolumeLevelScalar(level / 100,None)

def change_volume(direction):
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    if direction == "up":
        new_level = min(current +0.1, 1.0)
    else:
        new_level = max(current -0.1, 0.0)
    volume.SetMasterVolumeLevelScalar(new_level, None)
    print(f"Current volume after: {volume.GetMasterVolumeLevelScalar()}")



def set_brightness(level):
    level = max(0, min(level, 100))
    sbc.set_brightness(level)

def change_brightness(direction):
    current = sbc.get_brightness()[0]
    if direction == "up":
        new_level =min(current + 10, 100)
    else:
        new_level = max(current - 10, 0)
        sbc.set_brightness(new_level)