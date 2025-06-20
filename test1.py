import time
import requests
from typing import Dict, Any

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
def synthesize_prompt(user_state: Dict[str, Any], last_feedback: str = None) -> str:
    """
    Generate a Suno prompt based on user state and last feedback.
    """
    # Example: adapt prompt based on anxiety, sleep stage, and preference
    base_prompt = (
        "Generate a 5-minute ambient music piece designed for sleep induction. "
        "Use soft textures, slow evolving pads, and minimal melodic activity. "
        "The emotional tone should be calm, warm, and secure. "
        "Avoid percussive elements, tempo shifts, or sharp harmonic changes. "
        "The piece should start very quietly, gradually introduce gentle harmonics, and end with a fade-out to silence."
    )

    # Adjust prompt based on user state
    if user_state["anxiety_level"] >= 7:
        base_prompt = (
            "Create a music piece for patients with anxiety-driven insomnia. "
            "The emotional intention is to calm, ground, and reassure. "
            "Use consistent harmonic progressions, warm midrange instrumentation like soft strings and light piano, "
            "and avoid tension or dissonance. Keep tempo slow and steady, and prevent abrupt transitions."
        )
    if user_state["sleep_stage"] == "deep":
        base_prompt += " The music should fade out gradually as the user enters deep sleep."
    if user_state["sound_preference"]:
        base_prompt += f" Preferred instruments: {user_state['sound_preference']}."
    if last_feedback:
        base_prompt += f" Adjust according to feedback: {last_feedback}."

    return base_prompt

# ========== IV. Music Generation & Selection Layer ==========
def generate_music(prompt: str) -> Dict[str, Any]:
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
def play_music(audio_url: str):
    """
    Simulate music playback on a device.
    In production, integrate with your audio playback system.
    """
    print(f"Playing music: {audio_url}")

def record_session(user_state: Dict[str, Any], prompt: str, music_info: Dict[str, Any], feedback: str):
    """
    Record the session data for future personalization and analysis.
    """
    # In production, save to database or file
    print("Session recorded:", {
        "user_state": user_state,
        "prompt": prompt,
        "music_id": music_info.get("id"),
        "feedback": feedback
    })

def get_sleep_feedback(sensor_data: Dict[str, Any]) -> str:
    """
    Analyze sensor data to generate feedback for prompt adjustment.
    """
    # Example: if heart rate drops and movement is low, user is likely asleep
    if sensor_data["sleep_stage"] == "deep" and sensor_data["heart_rate"] < 60:
        return "User is in deep sleep, fade out music."
    elif sensor_data["anxiety_level"] > 7:
        return "User remains anxious, use even slower tempo and softer sounds."
    elif sensor_data["movement"] > 0.5:
        return "User is restless, try more calming music."
    else:
        return "Continue current strategy."

# ========== MAIN LOOP ==========
def main():
    """
    Main loop for passive music therapy system.
    """
    last_feedback = None
    for session in range(3):  # Simulate 3 music sessions
        print(f"\n--- Session {session+1} ---")
        # 1. Get real-time sensor data
        sensor_data = get_wearable_data()
        # 2. Build user embedding
        user_state = build_user_embedding(sensor_data)
        # 3. Synthesize prompt
        prompt = synthesize_prompt(user_state, last_feedback)
        print("Prompt:", prompt)
        # 4. Generate music
        music_data = generate_music(prompt)
        audio_url = music_data[0].get("audio_url", "N/A")
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
