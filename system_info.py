import psutil

def get_battery_status():
    battery = psutil.sensors_battery()
    if  battery is None:
        return "I couldn't detect battery on this device."
    percent = battery.percent
    plugged = battery.power_plugged
    status = "charging" if plugged else "not charging"
    return f"Battery is at {percent} percent, {status}"

def get_ram_usage():
    memory = psutil.virtual_memory()
    percent_used = memory.percent
    available_gb = round(memory.available / (1024 ** 3), 1)
    return f"RAM usage is at {percent_used} percent, with {available_gb} gigabytes free."