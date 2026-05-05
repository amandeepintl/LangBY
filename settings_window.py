"""
Langby - Settings Window
Glassmorphic settings GUI with collapsible dropdown selector.
"""

import os
import sys
import threading
import customtkinter as ctk

from config import load_config, save_config, set_auto_start, LANGUAGES, LANG_CODE_TO_NAME
from glass import apply_glass, GLASS_COLORS as G
from setup_wizard import DropdownSelector


def _get_asset_path(filename):
    if getattr(sys, '_MEIPASS', None):
        return os.path.join(sys._MEIPASS, 'assets', filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', filename)


class SettingsWindow:
    """Glassmorphic settings window for Langby."""

    _instance = None
    _instance_lock = threading.Lock()

    @classmethod
    def open(cls):
        with cls._instance_lock:
            if cls._instance is not None:
                try:
                    cls._instance.root.focus_force()
                    return
                except Exception:
                    cls._instance = None
            instance = cls()
            cls._instance = instance
        threading.Thread(target=instance._run, daemon=True).start()

    def __init__(self):
        self.root = None
        self.config = load_config()
        self.lang_names = sorted(LANGUAGES.keys())

    def _run(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Hidden persistent root — keeps Tcl alive
        self._hidden_root = ctk.CTk()
        self._hidden_root.withdraw()

        self.root = ctk.CTkToplevel(self._hidden_root)
        self.root.title("LangBY Settings")
        self.root.geometry("400x460")
        self.root.resizable(False, False)

        try:
            ico_path = _get_asset_path('icon.ico')
            if os.path.exists(ico_path):
                self.root.after(200, lambda: self.root.iconbitmap(ico_path))
        except Exception:
            pass

        apply_glass(self.root)
        self._build_ui()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._hidden_root.mainloop()

    def _build_ui(self):
        root = self.root

        # ── Header ──
        header = ctk.CTkFrame(root, fg_color="transparent")
        header.pack(fill="x", padx=28, pady=(20, 4))

        ctk.CTkLabel(
            header, text="⚙  LangBY Settings",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=G["accent_glow"],
        ).pack(anchor="w")

        ctk.CTkFrame(root, height=1, fg_color=G["divider"]).pack(fill="x", padx=28, pady=(10, 8))

        # ── Language (Collapsible Dropdown) ──
        lang_card = ctk.CTkFrame(root, fg_color=G["card"], corner_radius=12,
                                 border_width=1, border_color=G["card_border"])
        lang_card.pack(fill="x", padx=28)

        ctk.CTkLabel(
            lang_card, text="TARGET LANGUAGE",
            font=ctk.CTkFont(size=10, weight="bold"), text_color=G["text_muted"],
        ).pack(anchor="w", padx=14, pady=(12, 4))

        current_lang = self.config.get('target_language_name', 'Japanese')
        self.lang_var = ctk.StringVar(value=current_lang)
        DropdownSelector(
            lang_card, values=self.lang_names, default=current_lang,
            variable=self.lang_var, list_height=150, searchable=True,
        ).pack(fill="x", padx=14, pady=(0, 12))

        # ── Hotkeys (Glass Card) ──
        hotkey_card = ctk.CTkFrame(root, fg_color=G["card"], corner_radius=12,
                                   border_width=1, border_color=G["card_border"])
        hotkey_card.pack(fill="x", padx=28, pady=(10, 0))

        ctk.CTkLabel(
            hotkey_card, text="HOTKEYS",
            font=ctk.CTkFont(size=10, weight="bold"), text_color=G["text_muted"],
        ).pack(anchor="w", padx=14, pady=(12, 6))

        hotkeys_info = [
            ("Translate All Text", self.config.get('hotkey_translate_all_display', 'Ctrl + Shift + L')),
            ("Translate Selected", "Ctrl + Shift + K"),
        ]

        for label_text, key_text in hotkeys_info:
            row = ctk.CTkFrame(hotkey_card, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=2)

            ctk.CTkLabel(
                row, text=label_text,
                font=ctk.CTkFont(size=12), text_color=G["text"],
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=f"  {key_text}  ",
                font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                text_color=G["accent_glow"], fg_color=G["badge_bg"],
                corner_radius=6,
            ).pack(side="right")

        ctk.CTkFrame(hotkey_card, height=6, fg_color="transparent").pack()

        # ── Options ──
        opts_card = ctk.CTkFrame(root, fg_color=G["card"], corner_radius=12,
                                 border_width=1, border_color=G["card_border"])
        opts_card.pack(fill="x", padx=28, pady=(10, 0))

        ctk.CTkLabel(
            opts_card, text="OPTIONS",
            font=ctk.CTkFont(size=10, weight="bold"), text_color=G["text_muted"],
        ).pack(anchor="w", padx=14, pady=(12, 4))

        self.autostart_var = ctk.BooleanVar(value=self.config.get('auto_start', True))
        ctk.CTkSwitch(
            opts_card, text="  Start with Windows",
            font=ctk.CTkFont(size=12), variable=self.autostart_var,
            text_color=G["text"],
            progress_color=G["accent"],
            button_color="#FFFFFF", button_hover_color="#E0E0E0",
            fg_color=G["input_border"],
        ).pack(anchor="w", padx=14, pady=(0, 12))

        # ── Buttons ──
        btn_frame = ctk.CTkFrame(root, fg_color="transparent")
        btn_frame.pack(fill="x", padx=28, pady=(18, 14))

        ctk.CTkButton(
            btn_frame, text="Save",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=G["accent"], hover_color=G["accent_hover"],
            text_color="#FFFFFF", height=40, width=170, corner_radius=10,
            command=self._on_save,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_frame, text="Close",
            font=ctk.CTkFont(size=14),
            fg_color=G["btn_secondary"], hover_color=G["btn_sec_hover"],
            text_color=G["text_dim"],
            height=40, width=170, corner_radius=10,
            command=self._on_close,
        ).pack(side="right")

    def _on_save(self):
        lang_name = self.lang_var.get()
        lang_code = LANGUAGES.get(lang_name, 'ja')

        self.config['target_language'] = lang_code
        self.config['target_language_name'] = lang_name
        self.config['auto_start'] = self.autostart_var.get()

        save_config(self.config)
        set_auto_start(self.autostart_var.get())

        # Update tray icon tooltip
        try:
            import shared
            if shared.tray_icon:
                shared.tray_icon.title = f"LangBY — {lang_name}"
        except Exception:
            pass

        print(f"[LangBY] Settings saved: {lang_name} ({lang_code})")
        self._on_close()

    def _on_close(self):
        with self._instance_lock:
            SettingsWindow._instance = None
        try:
            if self.root:
                self.root.destroy()
        except Exception:
            pass
        try:
            if self._hidden_root:
                self._hidden_root.destroy()
        except Exception:
            pass

        # Show "Langby is running" reminder
        try:
            from splash import show_startup_splash
            config = load_config()
            show_startup_splash(
                hotkey_display=config.get('hotkey_translate_all_display', 'Ctrl + Shift + L'),
                lang_name=config.get('target_language_name', 'Japanese'),
            )
        except Exception:
            pass
