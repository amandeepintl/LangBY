"""
Langby - Global Hotkey Handler
Listens for global hotkeys and performs text translation in-place.

Hotkeys:
  Shift+L  -> Select ALL text in field, translate, paste back
  Ctrl+Shift+K -> Translate only SELECTED/highlighted text
"""

import time
import threading
import keyboard
import pyperclip
import winsound

from translator import translate
from config import load_config

# Lock to prevent concurrent translations
_lock = threading.Lock()


def _wait_for_keys_released():
    """Wait until all modifier keys and L are released."""
    timeout = time.time() + 0.5  # max 0.5 second wait
    while time.time() < timeout:
        if not (keyboard.is_pressed('shift') or keyboard.is_pressed('ctrl') or keyboard.is_pressed('l')):
            break
        time.sleep(0.005)
    time.sleep(0.02)


def _get_clipboard():
    """Safely read clipboard contents."""
    try:
        return pyperclip.paste()
    except Exception:
        return ''


def _set_clipboard(text):
    """Safely set clipboard contents."""
    try:
        pyperclip.copy(text)
    except Exception:
        pass


def _do_translate(select_all=True):
    """
    Core translation logic.
    
    Args:
        select_all: If True, sends Ctrl+A first to select all text.
                    If False, assumes text is already selected.
    """
    if not _lock.acquire(blocking=False):
        return  # Already translating

    try:
        config = load_config()
        if not config.get('enabled', True):
            return

        target_lang = config.get('target_language', 'ja')

        # Wait for the hotkey keys to be released
        _wait_for_keys_released()

        # Save current clipboard
        original_clipboard = _get_clipboard()

        # Clear clipboard so we can detect if copy worked
        _set_clipboard('')

        if select_all:
            # Select all text in the active field
            keyboard.press_and_release('ctrl+a')
            time.sleep(0.04)

        # Copy selected text
        keyboard.press_and_release('ctrl+c')
        time.sleep(0.06)

        # Read the copied text
        text = _get_clipboard()

        if not text or not text.strip():
            # Nothing was copied - restore clipboard and bail
            _set_clipboard(original_clipboard)
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            return

        # Translate
        result = translate(text, target_lang)

        if result is None:
            # Translation failed - restore original text and clipboard
            _set_clipboard(original_clipboard)
            keyboard.press_and_release('escape')  # deselect
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            return

        # Paste translated text (replaces the selected text)
        _set_clipboard(result)
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.04)

        # Success sound
        winsound.MessageBeep(winsound.MB_OK)

        # Restore original clipboard after a delay (in background)
        def restore():
            time.sleep(0.8)
            _set_clipboard(original_clipboard)

        threading.Thread(target=restore, daemon=True).start()

    except Exception as e:
        print(f"[Langby] Hotkey handler error: {e}")
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    finally:
        _lock.release()


def _on_translate_all():
    """Callback for Shift+L: select all text and translate."""
    threading.Thread(target=_do_translate, args=(True,), daemon=True).start()


def _on_translate_selected():
    """Callback for Ctrl+Shift+K: translate only selected text."""
    threading.Thread(target=_do_translate, args=(False,), daemon=True).start()


def register_hotkeys():
    """Register global hotkeys for translation."""
    config = load_config()
    hotkey_all = config.get('hotkey_translate_all', 'ctrl+shift+l')
    keyboard.add_hotkey(hotkey_all, _on_translate_all, suppress=True)
    keyboard.add_hotkey('ctrl+shift+k', _on_translate_selected, suppress=True)
    print(f"[Langby] Hotkeys registered: {hotkey_all} (translate all), ctrl+shift+k (translate selected)")


def unregister_hotkeys():
    """Remove all registered hotkeys."""
    keyboard.unhook_all_hotkeys()
    print("[Langby] Hotkeys unregistered")
