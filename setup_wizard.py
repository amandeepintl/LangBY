"""
Langby - First-Run Setup Wizard
Glassmorphic onboarding with searchable collapsible dropdown selectors.
"""

import os
import sys
import customtkinter as ctk
from PIL import Image
from config import LANGUAGES, save_config, set_auto_start, DEFAULT_CONFIG
from glass import apply_glass, GLASS_COLORS as G


def _get_asset_path(filename):
    if getattr(sys, '_MEIPASS', None):
        return os.path.join(sys._MEIPASS, 'assets', filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', filename)


ALL_LANGUAGES = sorted(LANGUAGES.keys())

HOTKEY_PRESETS = [
    "Ctrl + Shift + L",
    "Ctrl + Shift + T",
    "Ctrl + Alt + T",
    "Ctrl + Shift + J",
    "Ctrl + Alt + L",
]

HOTKEY_MAP = {
    "Ctrl + Shift + L": "ctrl+shift+l",
    "Ctrl + Shift + T": "ctrl+shift+t",
    "Ctrl + Alt + T":   "ctrl+alt+t",
    "Ctrl + Shift + J": "ctrl+shift+j",
    "Ctrl + Alt + L":   "ctrl+alt+l",
}


class DropdownSelector:
    """Collapsible dropdown with search bar and scrollable radio list."""

    def __init__(self, parent, values, default, variable, font=None,
                 list_height=220, searchable=False):
        self.parent = parent
        self.values = values
        self.variable = variable
        self.expanded = False
        self.searchable = searchable
        self.font = font or ctk.CTkFont(size=13)

        # Container
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")

        # Dropdown button (frame with text + arrow)
        self.btn_frame = ctk.CTkFrame(
            self.frame, fg_color=G["input_bg"], corner_radius=8,
            border_width=1, border_color=G["input_border"],
            height=40, cursor="hand2",
        )
        self.btn_frame.pack(fill="x")
        self.btn_frame.pack_propagate(False)

        self.btn_label = ctk.CTkLabel(
            self.btn_frame, text=f"  {default}",
            font=self.font, anchor="w",
            text_color=G["text"], fg_color="transparent",
        )
        self.btn_label.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self.arrow_label = ctk.CTkLabel(
            self.btn_frame, text="▾",
            font=ctk.CTkFont(size=14),
            text_color=G["text_muted"], fg_color="transparent",
            width=30,
        )
        self.arrow_label.pack(side="right", padx=(0, 8))

        # Make both labels clickable
        for widget in (self.btn_frame, self.btn_label, self.arrow_label):
            widget.bind("<Button-1>", lambda e: self._toggle())

        # Expandable panel (hidden by default)
        self.panel = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.list_height = list_height
        self._populated = False

        # Search entry (only if searchable)
        if self.searchable:
            self.search_var = ctk.StringVar()
            self.search_var.trace_add("write", self._on_search)
            self.search_entry = ctk.CTkEntry(
                self.panel, placeholder_text="🔍  Search languages...",
                textvariable=self.search_var,
                font=ctk.CTkFont(size=12),
                fg_color=G["bg"],
                border_color=G["input_border"],
                text_color=G["text"],
                placeholder_text_color=G["text_muted"],
                height=34, corner_radius=8,
            )
            self.search_entry.pack(fill="x", pady=(4, 4))

        # List frame (created now, populated lazily)
        use_scroll = len(values) > 8
        if use_scroll:
            self.list_frame = ctk.CTkScrollableFrame(
                self.panel, height=list_height, fg_color=G["input_bg"],
                corner_radius=8, border_width=1, border_color=G["card_border"],
                scrollbar_button_color=G["accent"],
                scrollbar_button_hover_color=G["accent_hover"],
            )
        else:
            self.list_frame = ctk.CTkFrame(
                self.panel, fg_color=G["input_bg"],
                corner_radius=8, border_width=1, border_color=G["card_border"],
            )
        self.list_frame.pack(fill="x")

        self.radio_buttons = {}

    def _populate(self):
        """Create radio buttons lazily on first expand."""
        if self._populated:
            return
        self._populated = True
        for val in self.values:
            btn = ctk.CTkRadioButton(
                self.list_frame, text=val, variable=self.variable, value=val,
                font=self.font,
                text_color=G["text"],
                fg_color=G["accent"],
                hover_color=G["accent_hover"],
                border_color=G["input_border"],
                command=lambda v=val: self._on_select(v),
            )
            btn.pack(anchor="w", padx=10, pady=3)
            self.radio_buttons[val] = btn

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def _toggle(self):
        if self.expanded:
            self.panel.pack_forget()
            self.arrow_label.configure(text="▾")
        else:
            self._populate()  # Lazy load on first open
            self.panel.pack(fill="x", pady=(4, 0))
            try:
                self.list_frame._parent_canvas.yview_moveto(0.0)
            except Exception:
                pass
            if self.searchable:
                self.search_entry.focus()
            self.arrow_label.configure(text="▴")
        self.expanded = not self.expanded

    def _on_select(self, value):
        self.btn_label.configure(text=f"  {value}")
        self.arrow_label.configure(text="▾")
        self.panel.pack_forget()
        self.expanded = False

    def _on_search(self, *args):
        query = self.search_var.get().lower().strip()
        for val, btn in self.radio_buttons.items():
            if query == "" or query in val.lower():
                btn.pack(anchor="w", padx=10, pady=3)
            else:
                btn.pack_forget()
        # Scroll to top after filtering
        try:
            self.list_frame._parent_canvas.yview_moveto(0.0)
        except Exception:
            pass


class SetupWizard:
    """Glassmorphic first-run setup wizard."""

    def __init__(self):
        self.result = None

    def run(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("LangBY — Setup")
        self.root.geometry("420x520")
        self.root.resizable(False, False)

        try:
            ico_path = _get_asset_path('icon.ico')
            if os.path.exists(ico_path):
                self.root.iconbitmap(ico_path)
        except Exception:
            pass

        apply_glass(self.root)
        self._build_ui()

        self.root.protocol("WM_DELETE_WINDOW", self._on_skip)
        self.root.mainloop()
        return self.result

    def _build_ui(self):
        root = self.root

        # ── Header ──
        header = ctk.CTkFrame(root, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(16, 0))

        try:
            logo_path = _get_asset_path('icon.png')
            if os.path.exists(logo_path):
                logo_img = ctk.CTkImage(light_image=Image.open(logo_path), size=(44, 44))
                ctk.CTkLabel(header, image=logo_img, text="").pack()
        except Exception:
            pass

        ctk.CTkLabel(
            header, text="Welcome to LangBY",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=G["accent_glow"],
        ).pack(pady=(4, 0))

        ctk.CTkLabel(
            header, text="Let's set up your instant translator.",
            font=ctk.CTkFont(size=11), text_color=G["text_dim"],
        ).pack(pady=(1, 0))

        ctk.CTkFrame(root, height=1, fg_color=G["divider"]).pack(fill="x", padx=30, pady=(10, 6))

        # ── Step 1: Language (searchable) ──
        card1 = ctk.CTkFrame(root, fg_color=G["card"], corner_radius=10,
                             border_width=1, border_color=G["card_border"])
        card1.pack(fill="x", padx=30)

        ctk.CTkLabel(
            card1, text="①  TARGET LANGUAGE",
            font=ctk.CTkFont(size=10, weight="bold"), text_color=G["text_muted"],
        ).pack(anchor="w", padx=12, pady=(8, 3))

        self.lang_var = ctk.StringVar(value="Japanese")
        DropdownSelector(
            card1, values=ALL_LANGUAGES, default="Japanese",
            variable=self.lang_var, list_height=160, searchable=True,
        ).pack(fill="x", padx=12, pady=(0, 8))

        # ── Step 2: Hotkey ──
        card2 = ctk.CTkFrame(root, fg_color=G["card"], corner_radius=10,
                             border_width=1, border_color=G["card_border"])
        card2.pack(fill="x", padx=30, pady=(6, 0))

        ctk.CTkLabel(
            card2, text="②  TRANSLATION HOTKEY",
            font=ctk.CTkFont(size=10, weight="bold"), text_color=G["text_muted"],
        ).pack(anchor="w", padx=12, pady=(8, 3))

        self.hotkey_var = ctk.StringVar(value="Ctrl + Shift + L")
        DropdownSelector(
            card2, values=HOTKEY_PRESETS, default="Ctrl + Shift + L",
            variable=self.hotkey_var,
            font=ctk.CTkFont(family="Consolas", size=12),
            list_height=120, searchable=False,
        ).pack(fill="x", padx=12, pady=(0, 8))

        # ── Step 3: Auto-start ──
        card3 = ctk.CTkFrame(root, fg_color=G["card"], corner_radius=10,
                             border_width=1, border_color=G["card_border"])
        card3.pack(fill="x", padx=30, pady=(6, 0))

        ctk.CTkLabel(
            card3, text="③  STARTUP",
            font=ctk.CTkFont(size=10, weight="bold"), text_color=G["text_muted"],
        ).pack(anchor="w", padx=12, pady=(8, 2))

        self.autostart_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(
            card3, text="  Launch with Windows",
            font=ctk.CTkFont(size=12), variable=self.autostart_var,
            text_color=G["text"],
            progress_color=G["accent"],
            button_color="#FFFFFF", button_hover_color="#E0E0E0",
            fg_color=G["input_border"],
        ).pack(anchor="w", padx=12, pady=(0, 8))

        # ── Button ──
        btn_frame = ctk.CTkFrame(root, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(12, 6))

        ctk.CTkButton(
            btn_frame, text="Get Started  →",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=G["accent"], hover_color=G["accent_hover"],
            text_color="#FFFFFF", height=40, corner_radius=10,
            command=self._on_start,
        ).pack(fill="x")

        ctk.CTkLabel(
            btn_frame, text="You can change these later from the tray icon.",
            font=ctk.CTkFont(size=9), text_color=G["text_muted"],
        ).pack(pady=(3, 0))

    def _on_start(self):
        lang_name = self.lang_var.get()
        lang_code = LANGUAGES.get(lang_name, "ja")
        hotkey_display = self.hotkey_var.get()
        hotkey_key = HOTKEY_MAP.get(hotkey_display, "ctrl+shift+l")

        self.result = {
            "target_language": lang_code,
            "target_language_name": lang_name,
            "hotkey_translate_all": hotkey_key,
            "hotkey_translate_all_display": hotkey_display,
            "auto_start": self.autostart_var.get(),
            "enabled": True,
            "first_run_done": True,
        }
        self.root.destroy()

    def _on_skip(self):
        self.result = DEFAULT_CONFIG.copy()
        self.result["first_run_done"] = True
        self.root.destroy()
