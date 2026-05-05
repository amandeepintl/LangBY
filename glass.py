"""
Langby - Glassmorphism Utilities
Shared glass effect helpers + warm earthy color palette for all Langby windows.
Uses Windows DWM API for acrylic blur + custom styling.
"""

import ctypes
import sys


def apply_glass(root, bg_color="#1a1510"):
    """
    Apply glassmorphism effect to a customtkinter window.
    """
    root.configure(fg_color=bg_color)
    root.attributes("-alpha", 0.96)

    root.update()
    try:
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        if not hwnd:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
        _set_dwm_acrylic(hwnd)
        _set_dwm_dark_mode(hwnd)
        _set_dwm_rounded_corners(hwnd)
    except Exception:
        pass


def _set_dwm_acrylic(hwnd):
    """Enable acrylic backdrop via DWM."""
    try:
        DWMWA_SYSTEMBACKDROP_TYPE = 38
        value = ctypes.c_int(3)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_SYSTEMBACKDROP_TYPE,
            ctypes.byref(value), ctypes.sizeof(value)
        )
    except Exception:
        try:
            class ACCENT_POLICY(ctypes.Structure):
                _fields_ = [
                    ("AccentState", ctypes.c_int),
                    ("AccentFlags", ctypes.c_int),
                    ("GradientColor", ctypes.c_uint),
                    ("AnimationId", ctypes.c_int),
                ]

            class WINCOMPATTRDATA(ctypes.Structure):
                _fields_ = [
                    ("Attribute", ctypes.c_int),
                    ("Data", ctypes.POINTER(ACCENT_POLICY)),
                    ("SizeOfData", ctypes.c_size_t),
                ]

            accent = ACCENT_POLICY()
            accent.AccentState = 3
            accent.GradientColor = 0x991a1510

            data = WINCOMPATTRDATA()
            data.Attribute = 19
            data.Data = ctypes.pointer(accent)
            data.SizeOfData = ctypes.sizeof(accent)

            ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))
        except Exception:
            pass


def _set_dwm_dark_mode(hwnd):
    try:
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        dark = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(dark), ctypes.sizeof(dark)
        )
    except Exception:
        pass


def _set_dwm_rounded_corners(hwnd):
    try:
        DWMWA_WINDOW_CORNER_PREFERENCE = 33
        value = ctypes.c_int(2)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(value), ctypes.sizeof(value)
        )
    except Exception:
        pass


# ── Warm Earthy Glass Color Palette ──
GLASS_COLORS = {
    # Backgrounds
    "bg":            "#1a1510",
    "card":          "#241f18",
    "card_border":   "#3d3228",
    "card_hover":    "#2e261d",

    # Inputs
    "input_bg":      "#1c1712",
    "input_border":  "#4a3d30",

    # Accent colors
    "accent":        "#8A5F41",       # Primary brown
    "accent_hover":  "#A77F60",       # Lighter brown
    "accent_glow":   "#CCD67F",       # Olive/lime highlight

    # Text
    "text":          "#F3E4C9",       # Cream
    "text_dim":      "#A77F60",       # Tan
    "text_muted":    "#6b5540",       # Muted brown

    # Misc
    "divider":       "#332a20",
    "badge_bg":      "#2a2218",
    "success":       "#CCD67F",       # Olive green
    "btn_secondary": "#2a2218",
    "btn_sec_hover": "#3d3228",
}
