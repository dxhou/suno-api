from typing import Dict, Any, Optional

# 结构化的Prompt模板库，支持多场景和多变量插值
PROMPT_LIBRARY: Dict[str, Dict[str, Any]] = {
    "general_sleep": {
        "template": (
            "Generate a 5-minute ambient music piece designed for sleep induction. "
            "Use soft textures, slow evolving pads, and minimal melodic activity. "
            "The emotional tone should be {emotion}. Avoid percussive elements, tempo shifts, or sharp harmonic changes. "
            "The piece should start very quietly, gradually introduce gentle harmonics, and end with a fade-out to silence."
        ),
        "default_vars": {
            "emotion": "calm, warm, and secure"
        }
    },
    "anxiety_insomnia": {
        "template": (
            "Create a music piece for patients with anxiety-driven insomnia. "
            "The emotional intention is to {emotion}. "
            "Use consistent harmonic progressions, warm midrange instrumentation like soft strings and light piano, "
            "and avoid tension or dissonance. Keep tempo slow and steady, and prevent abrupt transitions."
        ),
        "default_vars": {
            "emotion": "calm, ground, and reassure"
        }
    },
    "deep_sleep": {
        "template": (
            "Generate a music piece for deep sleep. "
            "The music should fade out gradually as the user enters deep sleep. "
            "Use very soft textures and minimal melodic activity."
        ),
        "default_vars": {}
    },
    "ptsd_hyperarousal": {
        "template": (
            "Generate a 6-minute looping ambient track for PTSD-related sleep disturbance. "
            "Emphasize stability, containment, and emotional safety. Use low-register pads, brown noise textures, and soft binaural elements. "
            "Avoid melodic surprises, loud instruments, or stereo effects that mimic external motion."
        ),
        "default_vars": {}
    },
    "sensory_fatigue": {
        "template": (
            "Create a minimalist ambient piece intended to reduce sensory fatigue. "
            "Prioritize sonic minimalism, use static drones, gentle sine wave tones, and avoid rhythmic complexity. "
            "Emotional target: neutral to slightly positive. No sharp attacks or sudden frequency changes."
        ),
        "default_vars": {}
    },
    "child_sleep_aid": {
        "template": (
            "Generate music for young individuals experiencing sleep trouble. "
            "Emotional tone: comforting, safe, and slightly magical. Include soft bells, lullaby-like motifs, and low-tempo background textures. "
            "Use a predictable structure, no surprises or tempo changes."
        ),
        "default_vars": {}
    }
}

def synthesize_prompt(
    template_entry: Dict[str, Any],
    user_state: Dict[str, Any],
    last_feedback: Optional[str] = None,
    extra_vars: Optional[Dict[str, Any]] = None
) -> str:
    """
    合成prompt，插入变量，支持健壮性和多轮反馈。
    :param template_entry: 选中的prompt模板及默认变量
    :param user_state: 用户状态字典
    :param last_feedback: 上一轮反馈（可选）
    :param extra_vars: 额外插值变量（可选）
    :return: 最终可用的prompt字符串
    """
    # 合并变量，优先级：extra_vars > user_state > default_vars
    merged_vars = dict(template_entry.get("default_vars", {}))
    merged_vars.update(user_state)
    if extra_vars:
        merged_vars.update(extra_vars)
    # 安全插值，缺失变量自动跳过
    try:
        prompt = template_entry["template"].format(**merged_vars)
    except KeyError as e:
        # 某些变量缺失，自动用空字符串代替
        import re
        def safe_format(template, vars):
            return re.sub(r"{(.*?)}", lambda m: str(vars.get(m.group(1), "")), template)
        prompt = safe_format(template_entry["template"], merged_vars)
    # 拼接反馈
    if last_feedback:
        prompt += f" Adjust according to feedback: {last_feedback}."
    # 拼接用户偏好
    if user_state.get("sound_preference"):
        prompt += f" Preferred instruments: {user_state['sound_preference']}."
    # 预留多轮参数调优接口（如有需要可在此处插入更多自适应内容）
    return prompt 