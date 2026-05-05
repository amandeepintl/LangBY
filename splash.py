"""
Langby - Startup Splash Notification
Glassmorphic notification window shown when Langby starts.
Auto-closes after a few seconds.
"""

import os
import sys
import threading
import customtkinter as ctk
from PIL import Image
from glass import apply_glass, GLASS_COLORS as G


def _get_asset_path(filename):
    if getattr(sys, '_MEIPASS', None):
        return os.path.join(sys._MEIPASS, 'assets', filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', filename)


def show_startup_splash(hotkey_display="Ctrl + Shift + L", lang_name="Japanese", auto_close_ms=2500):
    """Show a glassmorphic splash notification. Auto-closes. Non-blocking."""

    def _run():
        ctk.set_appearance_mode("dark")

        root = ctk.CTk()
        root.title("LangBY")
        root.geometry("390x195")
        root.resizable(False, False)

        # Set icon before overrideredirect
        try:
            ico_path = _get_asset_path('icon.ico')
            if os.path.exists(ico_path):
                root.iconbitmap(ico_path)
        except Exception:
            pass

        root.attributes("-topmost", True)
        root.overrideredirect(True)

        # Center on screen
        root.update_idletasks()
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw - 390) // 2
        y = (sh - 195) // 2
        root.geometry(f"390x195+{x}+{y}")

        # Transparent window background — hides black corners
        TRANSPARENT_KEY = "#010101"
        root.configure(fg_color=TRANSPARENT_KEY)
        root.attributes("-transparentcolor", TRANSPARENT_KEY)
        root.attributes("-alpha", 0.96)

        # ── Glass Container ──
        frame = ctk.CTkFrame(
            root, fg_color=G["card"], corner_radius=16,
            border_width=1, border_color=G["card_border"],
        )
        frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Logo + title row
        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x", padx=22, pady=(20, 0))

        try:
            logo_path = _get_asset_path('icon.png')
            if os.path.exists(logo_path):
                logo_img = ctk.CTkImage(light_image=Image.open(logo_path), size=(36, 36))
                ctk.CTkLabel(top, image=logo_img, text="").pack(side="left", padx=(0, 12))
        except Exception:
            pass

        ctk.CTkLabel(
            top, text="LangBY is running",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=G["accent_glow"],
        ).pack(side="left")

        ctk.CTkLabel(
            top, text="●", font=ctk.CTkFont(size=10),
            text_color=G["success"],
        ).pack(side="left", padx=(8, 0))

        # Language
        ctk.CTkLabel(
            frame, text=f"Translating to {lang_name}",
            font=ctk.CTkFont(size=13), text_color=G["text_dim"],
        ).pack(padx=22, pady=(10, 2), anchor="w")

        # Hotkey badge row
        hk = ctk.CTkFrame(frame, fg_color="transparent")
        hk.pack(fill="x", padx=22, pady=(4, 0))

        ctk.CTkLabel(hk, text="Press", font=ctk.CTkFont(size=12),
                     text_color=G["text_muted"]).pack(side="left")

        ctk.CTkLabel(
            hk, text=f"  {hotkey_display}  ",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color=G["accent_glow"], fg_color=G["badge_bg"],
            corner_radius=8,
        ).pack(side="left", padx=6)

        ctk.CTkLabel(hk, text="to translate", font=ctk.CTkFont(size=12),
                     text_color=G["text_muted"]).pack(side="left")

        # Accent bar
        ctk.CTkFrame(frame, height=3, fg_color=G["accent"],
                     corner_radius=2).pack(fill="x", padx=40, pady=(16, 12))

        # Auto-close
        root.after(auto_close_ms, root.destroy)

        # Draggable
        def start_drag(e):
            root._dx, root._dy = e.x, e.y

        def do_drag(e):
            root.geometry(f"+{root.winfo_x() + e.x - root._dx}+{root.winfo_y() + e.y - root._dy}")

        frame.bind("<Button-1>", start_drag)
        frame.bind("<B1-Motion>", do_drag)

        root.mainloop()

    threading.Thread(target=_run, daemon=True).start()
