This is your **Project D.A.R.T. Master Bible**.

This document contains three critical parts:

1.  **The Constitution:** Rules to keep the team consistent.
2.  **The Debugging Strategy:** How to catch bugs before they kill the project.
3.  **The Phased Roadmap:** Step-by-step tasks for every feature.

Save this as `MASTER_PLAN.md` in your project root.

-----

# 📘 Project D.A.R.T. - Master Execution Plan

## 🛡️ Part 1: Team Disciplines (The Constitution)

*To ensure code written by Member A works on Member B's computer.*

### 1\. The "Virtual Environment" Law

  * **Rule:** Never install libraries globally.
  * **Action:** Always verify your virtual environment is active (`(venv)` appears in terminal) before running `pip install`.
  * **Synchronization:** If you install a new library (e.g., `requests`), you **must** immediately run:
    ```bash
    pip freeze > requirements.txt
    ```
    *Teammates must run `pip install -r requirements.txt` when they pull your code.*

### 2\. The "Secret Key" Law

  * **Rule:** NEVER commit API keys (Google Cloud, Confluent) to GitHub.
  * **Action:**
      * Create a `.env` file in the root.
      * Add `.env` to your `.gitignore` file immediately.
      * Use `python-dotenv` to load keys in code.

### 3\. The "Persistence" Law (Reproducibility)

  * **Rule:** When testing, we want the "random" traffic to be the same every time so we can replicate bugs.
  * **Action:** Set a "Seed" for random generators in `config/settings.py`.
    ```python
    import random
    import numpy as np

    # If MODE is 'TEST', traffic is always the same. If 'LIVE', it varies.
    SEED = 42 
    random.seed(SEED)
    np.random.seed(SEED)
    ```

-----

## 🐞 Part 2: The Debugging System

*A centralized way to track errors across UI, Backend, and AI.*

Since this is a distributed system, a simple `print("error")` is not enough. We will build a custom **Logger** and a **UI Debug Mode**.

### Feature A: Centralized Logger (`utils/logger.py`)

Instead of `print()`, we use this. It saves logs to a file AND prints them with colors.

**Task:** Create `utils/` folder and `utils/logger.py`.

```python
import logging
import sys

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # 1. Print to Console (Terminal)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    
    # 2. Save to File (for reviewing later)
    file_handler = logging.FileHandler('debug_log.txt')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logger.addHandler(file_handler)
    
    return logger
```

*Usage in other files:*

```python
from utils.logger import get_logger
log = get_logger("TRAFFIC_GEN")

log.info("Generating cars...")
log.error("Confluent connection failed!")
```

### Feature B: The "Debug Mode" Toggle

In `config/settings.py`, add `DEBUG_MODE = True`.
In your Streamlit UI (`dashboard.py`), add this logic:

```python
if settings.DEBUG_MODE:
    with st.expander("🐞 Developer Console (Debug Mode)"):
        st.write("Raw JSON Data:", traffic_data_json)
        st.write("Last Gemini Response:", ai_response_text)
```

*Why? This allows you to see the raw data under the hood without breaking the beautiful UI.*

-----

## 🗺️ Part 3: The Roadmap (Phased Implementation)

### 🏁 Phase 0: Initialization (Done)

  * [x] Create Project Structure (`ui/`, `backend/`, `config/`).
  * [x] create `run.py` entry point.
  * [x] Create `requirements.txt`.

### 🏗️ Phase 1: The Visual Foundation (Frontend Focus)

*Goal: A working Dashboard that displays "Mock" (Fake) data.*

#### 1.1 Configuration Center

  * **File:** `config/settings.py`
  * **Detail:** Define Constants.
      * `MAP_CENTER`: [37.77, -122.41]
      * `REFRESH_RATE`: 2 seconds (for UI updates)

#### 1.2 The Mock Data Generator

  * **File:** `backend/simulation/traffic_gen.py`
  * **Detail:** Create a function `generate_mock_batch(n=10)` that returns a list of dictionaries.
      * *Structure:* `{'id': 'intersect_01', 'lat': ..., 'lon': ..., 'status': 'GREEN'}`
      * *Constraint:* Use `random.seed` so the dots appear in the same place every time you restart.

#### 1.3 Map Component Integration

  * **File:** `ui/components/map_widget.py`
  * **Detail:** Use `st.pydeck_chart` or `st.map`. Connect it to the Mock Data Generator.
  * **Debug Check:** Ensure dots appear on the screen.

#### 1.4 The Dashboard Layout

  * **File:** `ui/dashboard.py`
  * **Detail:** Create a 2-column layout (Map on Left, Stats on Right).

-----

### 🏭 Phase 2: The Data Pipeline (Confluent Cloud)

*Goal: Replace Mock Data with "Streaming" Data.*

#### 2.1 Confluent Setup (The Infrastructure)

  * **Platform:** Confluent Cloud Website.
  * **Task:** Create Cluster -\> Create Topic `traffic_raw` -\> Create API Keys.
  * **Task:** Save API keys in `.env` (NOT in Python files).

#### 2.2 The Producer (The Sender)

  * **File:** `backend/stream_engine/producer.py`
  * **Logic:**
    1.  Read Config (API Keys).
    2.  Loop forever (`while True`).
    3.  Call `generate_mock_batch`.
    4.  Convert to JSON.
    5.  Send to Topic `traffic_raw`.
  * **Debug Check:** Run this script in a separate terminal. Check Confluent Dashboard to see "Bytes/sec" go up.

#### 2.3 The Consumer (The Receiver)

  * **File:** `backend/stream_engine/consumer.py`
  * **Logic:**
    1.  Connect to Topic `traffic_raw`.
    2.  Poll for new messages.
    3.  Return the latest data to the main app.

-----

### 🧠 Phase 3: The AI Brain (Gemini Integration)

*Goal: Make the system "Think".*

#### 3.1 Google Cloud Setup

  * **Platform:** Google Cloud Console.
  * **Task:** Enable "Vertex AI API". Create Service Account Key. Save JSON key locally (add to `.gitignore`).

#### 3.2 The Gemini Client

  * **File:** `backend/ai_engine/client.py`
  * **Logic:**
      * Function: `ask_gemini(traffic_context)`
      * Input: A string summarizing traffic (e.g., "Intersection A is 90% full").
      * Output: A JSON string (e.g., `{"action": "switch_to_green"}`).

#### 3.3 Prompt Engineering

  * **File:** `backend/ai_engine/prompts.py`
  * **Detail:** Write the "System Prompt" that tells Gemini it is a City Traffic Controller.
      * *Constraint:* Tell Gemini to **ONLY** output JSON. No markdown, no chatting.

-----

### 🚀 Phase 4: Grand Integration (The Hackathon Winner)

*Goal: Connect Stream -\> AI -\> UI.*

#### 4.1 The "State Manager"

  * **File:** `ui/dashboard.py` (Session State)
  * **Logic:** Streamlit re-runs the whole script on every interaction. You need to store the data in `st.session_state` so it doesn't vanish.

#### 4.2 The Main Loop

  * **Logic:**
    1.  Dashboard auto-refreshes every 2 seconds.
    2.  It calls `consumer.get_latest_data()`.
    3.  It updates the Map.
    4.  **IF** congestion \> High -\> It calls `ai_engine.ask_gemini()`.
    5.  It displays the AI's Suggestion in the Sidebar.

-----

### 🚨 Phase 5: The "Emergency" Feature (Bonus)

*Goal: The winning feature.*

#### 5.1 Emergency Injector

  * **UI:** Add a button in Sidebar: "🔴 REPORT FIRE".
  * **Logic:** When clicked, it sends a special High Priority message to the Kafka Topic.

#### 5.2 AI Reaction

  * **Logic:** Update Prompt to say: "If event\_type is FIRE, turn all lights GREEN for the emergency route immediately."
