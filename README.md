# LangBY ✨

**Instant global translation at your fingertips.** Press a hotkey, and LangBY translates any text — in any app — right where you're typing.

<p align="center">
  <img src="assets/icon.png" alt="LangBY Logo" width="120">
</p>

---

## ⚡ Features

- 🌍 **35+ Languages** — Japanese, Korean, Spanish, Hindi, Arabic, and many more
- ⌨️ **Global Hotkeys** — Works in any application, any text field
- 🔍 **Searchable Language Picker** — Find your language instantly
- 🎨 **Glassmorphic UI** — Premium warm earthy design with blur effects
- 🚀 **Instant Translation** — Cached translator for lightning-fast results
- 🖥️ **System Tray** — Runs silently in the background
- ⚙️ **Setup Wizard** — One-time guided configuration on first launch
- 🔄 **Auto-Start** — Optionally launches with Windows

## 📥 Download

### One-Click Install
1. Go to [**Releases**](../../releases)
2. Download `LangBY.exe`
3. Run it — no installation needed!

### From Source
```bash
git clone https://github.com/AmanDeep/LangBY.git
cd LangBY
pip install -r requirements.txt
python langby.py
```

## 🎮 Usage

| Hotkey | Action |
|--------|--------|
| `Ctrl + Shift + L` | Select all text → Translate → Replace |
| `Ctrl + Shift + K` | Translate only selected/highlighted text |

### Quick Start
1. **Launch** `LangBY.exe`
2. **First run** — the Setup Wizard will ask for your target language and hotkey
3. **Type or select text** in any app
4. **Press the hotkey** — text is instantly translated in-place
5. **Right-click the tray icon** to change language, open settings, or quit

## 🖼️ Screenshots

### Setup Wizard
First-run guided configuration with searchable language dropdown.

### System Tray
Right-click for quick language switching, toggle, and settings.

### Settings
Full settings window with all options.

## 🏗️ Project Structure

```
LangBY/
├── langby.py            # Main entry point
├── config.py            # Settings & preferences manager
├── translator.py        # Translation engine (cached Google Translate)
├── hotkey_handler.py    # Global hotkey listener
├── tray_icon.py         # System tray icon & menu
├── settings_window.py   # Settings GUI
├── setup_wizard.py      # First-run wizard + DropdownSelector widget
├── splash.py            # Startup notification
├── glass.py             # Glassmorphism utilities & color palette
├── shared.py            # Shared state between components
├── assets/
│   ├── icon.png         # App icon (PNG)
│   └── icon.ico         # App icon (ICO)
├── requirements.txt     # Python dependencies
└── LICENSE              # MIT License
```

## 🔧 Building the Executable

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build
pyinstaller --noconsole --onefile --name LangBY --icon=assets/icon.ico --add-data "assets;assets" langby.py
```

The executable will be in `dist/LangBY.exe`.

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `customtkinter` | Modern themed Tkinter UI |
| `deep-translator` | Google Translate API (free) |
| `keyboard` | Global hotkey capture |
| `pyperclip` | Clipboard access |
| `pystray` | System tray icon |
| `Pillow` | Image handling |

## ⚙️ Configuration

Settings are stored in `%APPDATA%/Langby/config.json` and include:
- Target language
- Hotkey bindings
- Auto-start preference
- Enable/disable toggle

## 📄 License

[MIT License](LICENSE) — © 2026 Aman Deep

---

<p align="center">
  Made with ❤️ by <strong>Aman Deep</strong>
</p>
