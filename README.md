# FRIDAY — Personal AI Voice Assistant

A Jarvis-inspired, locally-running AI voice assistant built from scratch in Python. Voice in, voice out, real system control, persistent memory, a face-recognition lock screen, and a custom graphical desktop UI — no cloud backend, no subscription, runs entirely on your own machine.

Built as a solo learning project by a first-year CS student, typed by hand line by line — not copy-pasted — to actually understand every part of it.

![Status](https://img.shields.io/badge/status-active--development-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What Friday can actually do

- **Voice conversation** — wake-word activated ("Friday"), natural back-and-forth via Groq's LLM API, with persistent memory across restarts
- **System control** — volume, brightness, opening/closing apps, web search, YouTube, weather, time/date
- **Notes & expenses** — voice-logged, saved locally
- **Reminders** — background-threaded, fire in real time regardless of what else Friday is doing
- **Multi-command handling** — "close notepad and tell me the weather in Mohali" gets split and executed as two separate actions
- **AI-based command routing** — natural phrasing variations are handled by an LLM function-calling router, not brittle keyword matching
- **Screenshot vision** — "what's on my screen" describes your actual desktop using a vision-capable model
- **Face-recognition lock** — Friday starts locked on every launch; a live webcam face check unlocks it, and it auto-relocks after 5 minutes of no face detected
- **Hand-clap launcher** — clap once to launch Friday from closed, clap again to wake it, triple-clap to close it
- **Daily briefing** — "good morning" triggers an AI-phrased summary of weather, date, and today's reminders
- **Custom graphical UI** — a glowing orb interface (the "Core" UI) with real-time status states (idle/listening/thinking/speaking), a slide-in session log, and quick-action shortcuts
- **Typed chat option** — text commands go through the exact same processing pipeline as voice commands

## Architecture

```
Frontend (HTML/CSS/JS)  →  Flask (bridge)  →  Python backend modules
     templates/index.html      app_ui.py         voice.py, brain.py, apps.py, etc.
```

Friday runs as three concurrent threads: the Flask server (serves the UI and exposes a small JSON API), the main voice/command loop (`run_friday()`), and the `pywebview` window itself, which renders the frontend in a frameless native window instead of an actual browser tab.

### Module breakdown

| Module | Responsibility |
|---|---|
| `main.py` | Main loop, command routing/dispatch, wake-word handling, face-lock gating |
| `app_ui.py` | Flask server, API routes, pywebview window launcher |
| `voice.py` | Speech-to-text (`listen`), text-to-speech (`speak`), wake-word detection |
| `brain.py` | Groq client, conversation history load/save, general chat fallback |
| `ai_router.py` | LLM-based function-calling command router, multi-command splitting |
| `shared_state.py` | Shared state (status, conversation log, lock state) between threads |
| `apps.py`, `system_control.py`, `web_actions.py` | App open/close, volume/brightness, search/YouTube/weather/time |
| `notes.py`, `expenses.py`, `reminders.py` | Local JSON-backed feature modules |
| `system_info.py` | Battery/RAM status via `psutil` |
| `screen_vision.py` | Screenshot capture + vision-model description |
| `daily_briefing.py` | AI-phrased morning briefing |
| `face_enroll.py`, `face_train.py`, `face_login.py`, `face_lock_monitor.py` | Face-recognition lock system (enrollment, training, runtime check, background auto-relock) |
| `clap_launcher.py`, `clap_detector.py` | Standalone clap-based launch/wake/close via mic amplitude detection |

### Command routing flow

1. Voice or typed text comes in.
2. `split_commands()` (in `ai_router.py`) asks Groq to break the input into a JSON array of individual commands — so a single sentence with "and" in it becomes multiple actions.
3. Each sub-command goes to `handle_single_command()`.
4. That function first tries `route_command()` — an LLM function-calling call against a defined `TOOLS` schema — for anything with a matching tool (volume, weather, time, opening/closing apps, etc.).
5. Anything the router doesn't match falls through to a keyword-based `elif` chain covering everything not yet migrated to the router (brightness, search, YouTube, notes, expenses, reminders, screenshot vision).
6. Anything matching neither falls through to general conversational AI chat.

### Why LBPH over `face_recognition` for the lock system

The standard Python face-recognition library (`face_recognition`, built on `dlib`) has a genuinely poor Windows install story — not officially supported on Windows, requires CMake and Visual Studio Build Tools to compile from source, and common workarounds rely on unofficial precompiled wheels tied to old Python versions. Friday instead uses `opencv-contrib-python`'s built-in LBPH (Local Binary Patterns Histogram) face recognizer — a pure `pip install`, no compiling required, with strong benchmark accuracy for a single-user local setup.

One real operating constraint worth knowing: LBPH's accuracy is sensitive to lighting differences between enrollment and runtime. If recognition starts failing after previously working, check the lighting before assuming something broke.

## Setup

### Requirements

- Python 3.11
- Windows (the app control, volume/brightness, and packaging steps are Windows-specific)
- A webcam (for face-lock) and microphone (for voice)
- Free API keys: [Groq](https://console.groq.com) and [OpenWeatherMap](https://openweathermap.org/api)

### Installation

```bash
git clone https://github.com/seejalchalana-sc/FRIDAY-AI-ASSISTANT.git
cd FRIDAY-AI-ASSISTANT
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_key_here
OPENWEATHER_API_KEY=your_openweathermap_key_here
```

Never commit this file. It's already covered by `.gitignore`.

### Face enrollment (one-time setup)

```bash
python face_enroll.py
python face_train.py
```

`face_enroll.py` captures ~30 face samples via webcam. `face_train.py` trains the LBPH recognizer and saves `face_model.yml`. Both are one-time manual setup scripts, not part of the normal run loop.

### Running

```bash
python app_ui.py
```

This starts the Flask server, the voice loop, and opens the graphical window. Friday starts **locked** — say or type "check" to run the face-recognition unlock.

### Building a standalone .exe

```bash
pyinstaller --onefile --name Friday --add-data "templates;templates" app_ui.py --clean
```

Copy your `.env` file into the resulting `dist/` folder afterward — PyInstaller does not bundle it automatically, and the exe looks for `.env` in the same folder it's run from.

**Always use `--clean`** when rebuilding after changing anything in `templates/` or elsewhere. Without it, PyInstaller can silently reuse a cached build and skip your actual changes — the terminal will say `checking` instead of `Building` at each stage if this happens.

## Voice command reference

<details>
<summary>Click to expand full command list</summary>

**System**
- "volume up" / "volume down" / "set volume to [X] percent"
- "brightness up" / "brightness down" / "set brightness to [X] percent"
- "battery" — battery status
- "RAM" / "memory usage" — RAM status

**Apps & web**
- "open [notepad / calculator / chrome / vs code / paint / file explorer / word / excel / powerpoint / task manager / control panel / settings / cmd / spotify / edge / firefox]"
- "close [app name]"
- "search [for] X"
- "play X on youtube"

**Info**
- "what time is it" / "what's today's date"
- "what's the weather" / "weather in [city]"

**Notes & expenses**
- "take a note [that] X" / "read my notes" / "delete all notes"
- "I spent [X] on [category]" / "how much did I spend today / this month / total"

**Reminders**
- "remind me [in X minutes] to [Y]"

**Vision & briefing**
- "what's on my screen" / "describe my screen"
- "good morning" / "daily briefing"

**Security**
- "check" — runs the face-recognition unlock challenge
- Any command while locked returns a rejection line instead of executing

**Exit**
- "stop" / "exit" / "quit"

</details>

## Recurring bug patterns (worth knowing if you're reading the code)

A few mistakes showed up more than once across this project in different shapes — noting them here since they're genuinely useful patterns to watch for in any similarly-structured project, not just this one:

- **Trigger-phrase fallthrough.** An unmatched keyword phrase silently falls through to general AI chat, which will confidently claim to have done something it didn't. Always verify a new voice command actually worked with a separate check, don't just trust what Friday says back.
- **Specific conditions before general ones.** In an `if`/`elif` chain, a broad condition (like matching on the word "spend") placed before a narrower one (like "how much did I spend today") will always win and make the narrower branch unreachable.
- **Truthy bare strings.** `"good morning" or "daily_briefing" in command` is not what it looks like — Python evaluates `"good morning"` as always-truthy on its own, silently making the whole condition always true regardless of what was actually said.
- **Code placed after a blocking call never runs until that call returns.** `webview.start()`, `time.sleep()`, and similar blocking calls will silently prevent anything written after them (in the same execution path) from ever executing until the blocking call itself returns.
- **Cross-file variable name mismatches.** Python happily creates a new attribute on a module rather than erroring if a name is typo'd inconsistently across files — the bug only shows up as broken behavior, never a crash.
- **PyInstaller's build cache can silently skip a real rebuild.** If a build command completes with no errors but your changes still aren't reflected, check the terminal for `checking` vs `Building` at each stage, and use `--clean` to force a genuine rebuild.

## Roadmap

Currently in progress: a typed chat interface alongside voice, MediaPipe-based air-gesture control (cursor, click, virtual keyboard), invisible auto-start for the clap launcher, and a large backlog of brainstormed features ranging from practical (context-linked reminders, evening recaps) to ambitious (real phone calls via Twilio, cross-instance Friday-to-Friday communication).

## License

MIT — see [LICENSE](LICENSE).

## Author

Built by Seejal Chalana ([@CheejalXD](https://github.com/seejalchalana-sc)).
