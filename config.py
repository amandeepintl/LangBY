"""
Langby - Configuration Management
Handles saving/loading user preferences to %APPDATA%/Langby/config.json
"""

import json
import os
import sys

CONFIG_DIR = os.path.join(os.environ.get('APPDATA', '.'), 'Langby')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

DEFAULT_CONFIG = {
    "target_language": "ja",
    "target_language_name": "Japanese",
    "hotkey_translate_all": "ctrl+shift+l",
    "hotkey_translate_all_display": "Ctrl + Shift + L",
    "auto_start": True,
    "enabled": True,
    "first_run_done": False,
}

# Supported languages: display name -> language code
LANGUAGES = {
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
    "Hindi": "hi",
    "Thai": "th",
    "Vietnamese": "vi",
    "Indonesian": "id",
    "Turkish": "tr",
    "Polish": "pl",
    "Dutch": "nl",
    "Swedish": "sv",
    "Danish": "da",
    "Norwegian": "no",
    "Finnish": "fi",
    "Czech": "cs",
    "Romanian": "ro",
    "Hungarian": "hu",
    "Greek": "el",
    "Hebrew": "he",
    "Malay": "ms",
    "Filipino": "tl",
    "Ukrainian": "uk",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
    "Persian": "fa",
}

# Reverse lookup: code -> name
LANG_CODE_TO_NAME = {v: k for k, v in LANGUAGES.items()}


def load_config():
    """Load config from disk, returning defaults if file doesn't exist."""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(saved)
                return config
    except Exception:
        pass
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save config to disk."""
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Langby] Failed to save config: {e}")


def set_auto_start(enabled):
    """Add or remove Langby from Windows startup via registry."""
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_path, 0,
            winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
        )

        if enabled:
            # Find the pythonw.exe in the venv or system
            script_dir = os.path.dirname(os.path.abspath(__file__))
            venv_pythonw = os.path.join(script_dir, 'venv', 'Scripts', 'pythonw.exe')
            if os.path.exists(venv_pythonw):
                python_exe = venv_pythonw
            else:
                python_exe = sys.executable.replace('python.exe', 'pythonw.exe')
            
            script_path = os.path.join(script_dir, 'langby.py')
            winreg.SetValueEx(
                key, "LangBY", 0, winreg.REG_SZ,
                f'"{python_exe}" "{script_path}"'
            )
        else:
            try:
                winreg.DeleteValue(key, "LangBY")
            except FileNotFoundError:
                pass

        winreg.CloseKey(key)
    except Exception as e:
        print(f"[Langby] Failed to set auto-start: {e}")
