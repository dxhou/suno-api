# Passive Music Therapy System Demo

## Overview

This demo implements a passive music therapy system for insomnia and anxiety relief, using Suno API for AI-generated music. The system simulates wearable device data, generates personalized music prompts, calls the Suno API, and adapts music playback based on simulated physiological feedback.

## Features

- Simulates real-time physiological data (heart rate, HRV, sleep stage, movement, anxiety level, user preference)
- Builds a user state vector for personalized music generation
- Dynamically synthesizes prompts for Suno API based on user state and feedback
- Calls Suno API to generate sleep/relaxation music
- Simulates music playback and feedback loop
- Records each session for future personalization

## Requirements

- Python 3.7+
- `requests` library (`pip install requests`)
- A running Suno API service (local or remote)

## How to Run

1. **Install dependencies:**
   ```bash
   pip install requests
   ```

2. **Configure Suno API endpoint:**
   - Edit the `SUNO_API_BASE` variable in the script to match your Suno API endpoint (e.g., `http://localhost:3000`).

3. **Run the demo:**
   ```bash
   python music_therapy_demo.py
   ```

4. **Observe the output:**
   - The script will simulate three music therapy sessions, print the generated prompts, play (simulate) the music, and show feedback and session records.

## Customization

- **Integrate with real wearable devices:**  
  Replace the `get_wearable_data()` function with actual device API calls.
- **Integrate with real playback system:**  
  Replace the `play_music()` function with your audio playback logic.
- **Persist session data:**  
  Modify `record_session()` to save data to a database or file for long-term tracking and personalization.

## Example Output

```
--- Session 1 ---
Prompt: Generate a 5-minute ambient music piece designed for sleep induction. ...
Playing music: http://localhost:3000/audio/xxxxxx
Feedback: Continue current strategy.
Session recorded: {...}
...
```

## Notes

- This demo is for research and prototyping purposes.
- For production, ensure secure API handling, error management, and privacy protection for user data. 