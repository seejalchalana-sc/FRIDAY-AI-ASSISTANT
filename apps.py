import subprocess

def open_app(app_name):
    apps = {
         "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "chrome.exe",
        "vs code": "code",
        "paint": "mspaint.exe",
        "file explorer": "explorer.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "task manager": "taskmgr.exe",
        "control panel": "control.exe",
        "settings": "ms-settings:",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "spotify": "spotify.exe",
        "edge": "msedge.exe",
        "firefox": "firefox.exe"
    }

    app_command = apps.get(app_name)
    if app_command:
        try:
            subprocess.Popen(app_command)
            return True
        except Exception as e:
            print(f"Error opening {app_name}: {e}")
            return False
    return False

def close_app(app_name):
    process_names = {
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe",
        "chrome": "chrome.exe",
        "vs code": "Code.exe",
        "paint": "mspaint.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "spotify": "spotify.exe",
        "edge": "msedge.exe",
        "firefox": "firefox.exe"
    }
    process = process_names.get(app_name)
    if process:
        try:
            subprocess.run(f"taskkill /IM {process} /F", shell=True, check=True)
            return True
        except Exception as e:
            print(f"Error closing {app_name}: {e}")
            return False
    return False