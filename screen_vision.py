import os
import base64
import re
from PIL import ImageGrab
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def take_screenshot():
    """captures the current screen and saves it as a temp file."""
    screenshot = ImageGrab.grab()
    screenshot_path = "temp_screenshot.png"
    screenshot.save(screenshot_path)
    return screenshot_path

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def describe_screen():
    """takes a ss and asksGroq's" vision model to describe it"""
    screenshot_path = take_screenshot()
    base64_image = encode_image(screenshot_path)

    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type":"text", "text": "describe what's currently on the screen briefly and naturally, as if telling someone what you see. focus on the main application or content visible."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=1, 
        max_completion_tokens=800,
        top_p=1,
        stream=False
    )
    os.remove(screenshot_path)  # clean up the temp file
    raw_response = completion.choices[0].message.content
    #print("RAW RESPONSE:", raw_response)  #temp debug line
    cleaned_response = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL)
    cleaned_response = re.sub(r'<think>.*', '', cleaned_response, flags=re.DOTALL)
    cleaned_response = cleaned_response.strip()
    return cleaned_response

if __name__ == "__main__":
    print(describe_screen())
    