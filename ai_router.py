from brain import client
import json
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "set_volume",
            "description": "Set the system volume to a specific percentage",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {"type": "integer", "description": "Volume level from 0 to 100"}
                },
                "required": ["level"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "change_volume",
            "description": "Increase or decrease volume by a step",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {"type": "string", "enum": ["up", "down"]}
                },
                "required": ["direction"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_info",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name, e.g. Mohali"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time_info",
            "description": "Get the current time",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_application",
            "description": "Open an application on the computer",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "Name of the app, e.g. notepad, chrome, calculator"}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "close_application",
            "description": "Close an application that is currently open on the computer",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "Name of the app to close, e.g. notepad, chrome, calculator"}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_note",
            "description": "Save a note for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The content of the note"}
                },
                "required": ["text"]
            }
        }
    }
]


def route_command(command, available_functions):
    messages = [
        {"role": "system", "content": "You are Friday's command router. Analyze the user's request and call the most appropriate function. If no function matches, respond normally without calling any function."},
        {"role": "user", "content": command}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments) or {}
        if function_args is None:
            function_args = {}


        if function_name in available_functions:
            result = available_functions[function_name](**function_args)
            return result

    return None

def split_commands(text):
    messages = [
        {
            "role": "system",
            "content": (
                "You split spoken commands into a list of separate individual commands. "
                "Return ONLY a JSON array of strings, nothing else — no explanation, no markdown. "
                "If the text is only one command, return a list with just that one item. "
                "Example input: 'open notepad and tell me the weather' "
                "Example output: [\"open notepad\", \"tell me the weather\"]"
            )
        },
        {"role": "user", "content": text}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )

    raw = response.choices[0].message.content.strip()

    try:
        commands = json.loads(raw)
        if isinstance(commands, list) and len(commands)> 0:
            return commands
    except json.JSONDecodeError:
        pass

    return [text]