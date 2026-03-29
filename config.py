import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Paths ---
AVATARS_DIR  = os.path.join(BASE_DIR, "assets", "avatars")
PHOTOS_DIR   = os.path.join(BASE_DIR, "assets", "photos")
QUOTES_FILE  = os.path.join(BASE_DIR, "assets", "quotes.txt")
LOG_FILE     = os.path.join(BASE_DIR, "data", "log.txt")
ENV_FILE     = os.path.join(BASE_DIR, ".env")

# --- Weather ---
WEATHER_CITY        = "Centreville,VA,US"
WEATHER_UNITS       = "imperial"          # Fahrenheit
WEATHER_REFRESH_MIN = 30

# --- Photo panel ---
PHOTO_CYCLE_MIN = 10

# --- Pomodoro ---
POMODORO_WORK_MIN  = 25
POMODORO_BREAK_MIN = 5

# --- Dark retro color palette ---
COLORS = {
    "bg":          "#0c0c12",   # very dark blue-black (window bg)
    "panel_bg":    "#13131f",   # panel background
    "border":      "#252538",   # panel border
    "top_bg":      "#0f0f1a",   # top bar background
    "accent":      "#d4900f",   # amber / gold
    "accent_dim":  "#7a5208",   # darker amber (button bg)
    "text":        "#ddd0b8",   # warm cream
    "text_dim":    "#605040",   # muted / secondary text
    "text_bright": "#ffc840",   # bright gold
    "text_head":   "#c89030",   # section headers
    "success":     "#45c46a",   # retro green (checkmarks, saved)
    "danger":      "#e04545",   # red
    "timer_work":  "#38b8e0",   # cyan (work mode)
    "timer_break": "#45c46a",   # green (break mode)
    "btn_bg":      "#1a1a2a",   # button background
    "btn_active":  "#252540",   # button active/hover
    "sep":         "#1d1d30",   # separator lines
}

# --- Font ---
# Courier is available on all Pi/Linux systems; gives retro monospace feel
F = "Courier"
