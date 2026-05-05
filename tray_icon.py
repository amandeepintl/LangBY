"""
Langby - System Tray Icon
Creates a persistent system tray icon with a right-click menu for
language selection, toggling, and settings access.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem, Menu

from config import load_config, save_config, LANGUAGES, LANG_CODE_TO_NAME


def _get_asset_path(filename):
    """Get asset path that works both in dev and PyInstaller bundle."""
    if getattr(sys, '_MEIPASS', None):
        return os.path.join(sys._MEIPASS, 'assets', filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', filename)


def _create_fallback_icon(enabled=True):
    """Create a simple icon programmatically as fallback."""
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Warm brown circle matching our color scheme
    color = (138, 95, 65) if enabled else (100, 100, 100)
    draw.ellipse([4, 4, size - 4, size - 4], fill=color)

    # Letter "L" in cream
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except Exception:
        font = ImageFont.load_default()

    draw.text((size // 2, size // 2), "L", fill=(243, 228, 201), font=font, anchor="mm")
    return img


def _load_icon(enabled=True):
    """Load the app icon from assets, falling back to generated icon."""
    try:
        icon_path = _get_asset_path('icon.png')
        if os.path.exists(icon_path):
            img = Image.open(icon_path).convert('RGBA')
            if not enabled:
                img = img.convert('LA').convert('RGBA')
            return img
    except Exception:
        pass
    return _create_fallback_icon(enabled)


def create_tray_icon(on_settings_click, on_quit_click, on_toggle_click, on_language_change):
    """
    Create and return a pystray Icon object.
    """
    config = load_config()
    enabled = config.get('enabled', True)
    current_lang = config.get('target_language_name', 'Japanese')

    # Build language submenu with popular languages
    popular_langs = [
        "Japanese", "Korean", "Chinese (Simplified)", "Spanish",
        "French", "German", "Russian", "Arabic", "Hindi", "Portuguese",
        "Italian", "Thai", "Vietnamese", "Turkish",
    ]

    def make_lang_callback(code, name):
        def callback(icon, item):
            on_language_change(code, name)
            icon.title = f"LangBY — {name}"
        return callback

    lang_items = []
    for name in popular_langs:
        code = LANGUAGES.get(name)
        if code:
            lang_items.append(
                MenuItem(
                    name,
                    make_lang_callback(code, name),
                    checked=lambda item, n=name: load_config().get('target_language_name') == n
                )
            )

    lang_items.append(Menu.SEPARATOR)
    lang_items.append(MenuItem("More Languages...", lambda icon, item: on_settings_click()))

    def get_status_text(item):
        cfg = load_config()
        lang = cfg.get('target_language_name', 'Japanese')
        state = "ON" if cfg.get('enabled', True) else "OFF"
        return f"Target: {lang}  [{state}]"

    def get_toggle_text(item):
        cfg = load_config()
        return "Disable" if cfg.get('enabled', True) else "Enable"

    menu = Menu(
        MenuItem(get_status_text, None, enabled=False),
        Menu.SEPARATOR,
        MenuItem("Language", Menu(*lang_items)),
        Menu.SEPARATOR,
        MenuItem(get_toggle_text, lambda icon, item: on_toggle_click()),
        MenuItem("Settings", lambda icon, item: on_settings_click()),
        Menu.SEPARATOR,
        MenuItem("Quit LangBY", lambda icon, item: on_quit_click()),
    )

    icon = pystray.Icon(
        name="LangBY",
        icon=_load_icon(enabled),
        title=f"LangBY — {current_lang}",
        menu=menu
    )

    return icon
