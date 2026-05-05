"""
LangBY - Instant Global Translation Hotkey App
Main entry point. Wires together hotkey listener, system tray, and settings.
On first run, shows a setup wizard for language, hotkey, and auto-start.
"""

import sys
import os

# Ensure the script directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config, save_config, set_auto_start
from hotkey_handler import register_hotkeys, unregister_hotkeys
from tray_icon import create_tray_icon
from settings_window import SettingsWindow
from splash import show_startup_splash
import shared


def main():
    """Launch Langby."""
    print("[LangBY] Starting up...")

    # Load config
    config = load_config()

    # ── First-run setup wizard ──
    if not config.get('first_run_done', False):
        print("[LangBY] First run detected — opening setup wizard...")
        from setup_wizard import SetupWizard
        wizard = SetupWizard()
        result = wizard.run()

        if result:
            config = result
            save_config(config)
            if config.get('auto_start', True):
                set_auto_start(True)
            else:
                set_auto_start(False)
            print(f"[LangBY] Setup complete: {config.get('target_language_name')} / {config.get('hotkey_translate_all')}")
        else:
            config['first_run_done'] = True
            save_config(config)
    else:
        # Not first run — apply saved auto-start
        if config.get('auto_start', True):
            set_auto_start(True)

    # Register global hotkeys
    register_hotkeys()

    # Show startup splash notification
    hotkey_display = config.get('hotkey_translate_all_display', 'Ctrl + Shift + L')
    lang_name = config.get('target_language_name', 'Japanese')
    show_startup_splash(hotkey_display=hotkey_display, lang_name=lang_name)

    # Callbacks for the tray icon
    def on_settings():
        SettingsWindow.open()

    def on_quit():
        print("[LangBY] Shutting down...")
        unregister_hotkeys()
        icon.stop()
        os._exit(0)  # Force-kill all threads

    def on_toggle():
        cfg = load_config()
        cfg['enabled'] = not cfg.get('enabled', True)
        save_config(cfg)
        state = "enabled" if cfg['enabled'] else "disabled"
        print(f"[LangBY] Translation {state}")

    def on_language_change(lang_code, lang_name):
        cfg = load_config()
        cfg['target_language'] = lang_code
        cfg['target_language_name'] = lang_name
        save_config(cfg)
        print(f"[LangBY] Language changed to {lang_name} ({lang_code})")

    # Create and run the system tray icon (this blocks)
    global _tray_icon
    icon = create_tray_icon(
        on_settings_click=on_settings,
        on_quit_click=on_quit,
        on_toggle_click=on_toggle,
        on_language_change=on_language_change
    )
    shared.tray_icon = icon

    print("[LangBY] Running in system tray. Right-click the icon for options.")
    icon.run()

    print("[LangBY] Exited.")


if __name__ == '__main__':
    main()
