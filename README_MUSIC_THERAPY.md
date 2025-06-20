# Music Therapy AI Demo - User & Developer Guide

---

## Project Overview

This project demonstrates a closed-loop, passive music therapy system powered by Suno's music generation API and (simulated) wearable device data. The system dynamically generates, delivers, and adapts sleep or anxiety-relief music based on real-time physiological signals and user feedback, aiming to improve sleep quality and emotional well-being.

---

## Installation

1. **Python Version:** Python 3.8 or higher is recommended.
2. **Dependencies:**

```bash
pip install requests
```

---

## How to Run

1. Start the Suno API service (see official documentation for setup).
2. Configure the `SUNO_API_BASE` variable in `music_therapy_demo.py` if needed.
3. Run the main demo:

```bash
python music_therapy_demo.py
```

---

## Code Structure & Module Responsibilities

The codebase is organized for clarity, modularity, and easy extension. Below is an overview of the main modules and their responsibilities:

### 1. `music_therapy_demo.py` (Main Logic)

- **Sensor Input Layer** (`get_wearable_data`):
  - Simulates or fetches real-time physiological data (heart rate, HRV, sleep stage, movement, anxiety level, user preference).
  - In production, replace with actual device API calls.

- **User Modeling Layer** (`build_user_embedding`):
  - Converts raw sensor data into a structured user state vector for downstream personalization.

- **Prompt Synthesis & Scheduling** (`select_prompt_template`, `build_prompt`):
  - Selects the most appropriate prompt template from the prompt library based on user state (e.g., anxiety level, sleep stage).
  - Interpolates user state and feedback into the prompt for personalized music generation.

- **Music Generation & Selection** (`generate_music`):
  - Calls the Suno API to generate music using the synthesized prompt.
  - Handles API errors gracefully.

- **Push & Adaptive Feedback Layer** (`play_music`, `get_sleep_feedback`, `record_session`):
  - Simulates music playback (replace with actual playback integration as needed).
  - Analyzes updated sensor data to generate feedback for the next prompt.
  - Records session data for future personalization and analysis (extend to database/file as needed).

- **Main Loop** (`main`):
  - Orchestrates the above layers in a closed feedback loop for multiple sessions.
  - Demonstrates how the system adapts music based on real-time feedback.

### 2. `prompt_library.py` (Prompt Library & Synthesis)

- **PROMPT_LIBRARY**:
  - A structured dictionary of prompt templates for different therapy scenarios (e.g., general sleep, anxiety insomnia, deep sleep, PTSD, sensory fatigue, child sleep aid).
  - Each template supports variable interpolation for fine-grained control.

- **synthesize_prompt**:
  - Merges default variables, user state, and extra variables for robust prompt generation.
  - Handles missing variables gracefully.
  - Appends user feedback and preferences to the prompt for multi-round adaptation.
  - Extension point: Add more templates, variables, or logic for advanced personalization.

---

## How to Extend the System

- **Add New Therapy Scenarios:**
  - Edit `prompt_library.py` and add new entries to `PROMPT_LIBRARY` with your own templates and variables.
  - Update `select_prompt_template` in `music_therapy_demo.py` to route user states to new templates.

- **Integrate Real Wearable Devices:**
  - Replace the logic in `get_wearable_data()` with actual device API calls.

- **Persist Session Data:**
  - Modify `record_session()` to write to a database or file for long-term user modeling and analytics.

- **Advanced Feedback Loops:**
  - Enhance `get_sleep_feedback()` to use more sophisticated analysis or machine learning for feedback.
  - Use the `extra_vars` argument in `synthesize_prompt` for more dynamic prompt adaptation.

- **Front-End or API Integration:**
  - Build a web/mobile interface to visualize sessions, adjust parameters, or interact with the system in real time.

---

## FAQ

- **Q: What if the `requests` library is missing?**
  - A: Run `pip install requests` to install it.
- **Q: How do I connect to real wearable devices?**
  - A: Replace the `get_wearable_data()` function with your device's API integration.
- **Q: How do I add more therapy scenarios or prompt types?**
  - A: Add new templates in `prompt_library.py` and update the selection logic in `music_therapy_demo.py`.
- **Q: How do I persist user/session data?**
  - A: Extend `record_session()` to write to a file or database.

---

## Contact & Support

For questions, customization, or collaboration, please contact the project maintainer. 