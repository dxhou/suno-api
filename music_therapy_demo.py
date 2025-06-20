import time
import requests
from typing import Dict, Any, List, Optional
from prompt_library import PROMPT_LIBRARY, synthesize_prompt

# ========== CONFIGURATION ==========
SUNO_API_BASE = "http://localhost:3000"  # Replace with your Suno API endpoint

# ========== I. Sensor Input Layer ==========
def get_wearable_data() -> Dict[str, Any]:
    """
    Simulate fetching real-time physiological data from a wearable device.
    In production, replace this with actual device API calls.
    """
    # Example: heart rate, HRV, sleep stage, movement
    return {
        "heart_rate": 68,         # bpm
        "hrv": 45,                # ms
        "sleep_stage": "light",   # "awake", "light", "deep"
        "movement": 0.1,          # g-force or similar
        "anxiety_level": 6,       # 1-10 scale
        "user_preference": "piano, ambient"
    }

# ========== II. User Modeling Layer ==========
def build_user_embedding(sensor_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a user state vector from sensor and questionnaire data.
    """
    return {
        "HRV": sensor_data["hrv"],
        "heart_rate": sensor_data["heart_rate"],
        "sleep_stage": sensor_data["sleep_stage"],
        "anxiety_level": sensor_data["anxiety_level"],
        "sound_preference": sensor_data["user_preference"]
    }

# ========== III. Prompt Synthesis & Scheduling ==========
def select_prompt_template(user_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Select the most appropriate prompt template based on user state.
    """
    if user_state["anxiety_level"] >= 7:
        return PROMPT_LIBRARY["anxiety_insomnia"]
    elif user_state["sleep_stage"] == "deep":
        return PROMPT_LIBRARY["deep_sleep"]
    # 可扩展更多分支
    return PROMPT_LIBRARY["general_sleep"]

def build_prompt(user_state: Dict[str, Any], last_feedback: Optional[str] = None) -> str:
    """
    Build the final prompt string for music generation.
    """
    template = select_prompt_template(user_state)
    return synthesize_prompt(template, user_state, last_feedback)

# ========== IV. Music Generation & Selection Layer ==========
def generate_music(prompt: str) -> List[Dict[str, Any]]:
    """
    Call Suno API to generate music based on the prompt.
    """
    url = f"{SUNO_API_BASE}/api/generate"
    payload = {
        "prompt": prompt,
        "make_instrumental": True,
        "wait_audio": True
    }
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return response.json()

# ========== V. Push & Adaptive Feedback Layer ==========
def play_music(audio_url: str) -> None:
    """
    Simulate music playback on a device.
    In production, integrate with your audio playback system.
    """
    print(f"Playing music: {audio_url}")

def record_session(user_state: Dict[str, Any], prompt: str, music_info: Dict[str, Any], feedback: str) -> None:
    """
    Record the session data for future personalization and analysis.
    """
    # In production, save to database or file
    print("Session recorded:", {
        "user_state": user_state,
        "prompt": prompt,
        "music_id": music_info.get("id"),
        "audio_url": music_info.get("audio_url"),
        "feedback": feedback
    })

def get_sleep_feedback(sensor_data: Dict[str, Any]) -> str:
    """
    Analyze sensor data to generate feedback for prompt adjustment.
    """
    if sensor_data["sleep_stage"] == "deep" and sensor_data["heart_rate"] < 60:
        return "User is in deep sleep, fade out music."
    elif sensor_data["anxiety_level"] > 7:
        return "User remains anxious, use even slower tempo and softer sounds."
    elif sensor_data["movement"] > 0.5:
        return "User is restless, try more calming music."
    else:
        return "Continue current strategy."

# ========== MAIN LOOP ==========
def main() -> None:
    """
    Main loop for passive music therapy system.
    """
    last_feedback: Optional[str] = None
    for session in range(3):  # Simulate 3 music sessions
        print(f"\n--- Session {session+1} ---")
        # 1. Get real-time sensor data
        sensor_data = get_wearable_data()
        # 2. Build user embedding
        user_state = build_user_embedding(sensor_data)
        # 3. Synthesize prompt
        prompt = build_prompt(user_state, last_feedback)
        print("Prompt:", prompt)
        # 4. Generate music
        try:
            music_data = generate_music(prompt)
            audio_url = music_data[0].get("audio_url", "N/A")
        except Exception as e:
            print(f"Music generation failed: {e}")
            break
        # 5. Play music
        play_music(audio_url)
        # 6. Wait and simulate feedback (in real system, poll device data)
        time.sleep(2)  # Simulate playback time
        # 7. Get feedback from device
        sensor_data = get_wearable_data()  # In real use, get updated data
        last_feedback = get_sleep_feedback(sensor_data)
        print("Feedback:", last_feedback)
        # 8. Record session
        record_session(user_state, prompt, music_data[0], last_feedback)
        # 9. If user is asleep, stop music
        if "deep sleep" in last_feedback:
            print("User asleep, stopping music.")
            break

if __name__ == "__main__":
    main() 