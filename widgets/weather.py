import tkinter as tk
import os
import datetime
import threading

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from config import COLORS, F, ENV_FILE, WEATHER_CITY, WEATHER_UNITS, WEATHER_REFRESH_MIN

# Unicode weather icons (safe subset, works on Pi with default fonts)
ICONS = {
    "Clear":        "☀",
    "Clouds":       "☁",
    "Rain":         "⛆",
    "Drizzle":      "⛆",
    "Thunderstorm": "⛈",
    "Snow":         "❄",
    "Mist":         "~",
    "Fog":          "~",
    "Haze":         "~",
    "Smoke":        "~",
    "Dust":         "~",
    "Sand":         "~",
    "Ash":          "~",
    "Squall":       "~",
    "Tornado":      "!",
}


def _read_api_key():
    """Read OPENWEATHER_API_KEY from .env file."""
    if not os.path.exists(ENV_FILE):
        return None
    try:
        with open(ENV_FILE) as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("OPENWEATHER_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip("\"'")
                    if key and key != "your_api_key_here":
                        return key
    except Exception:
        pass
    return None


class WeatherPanel(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["panel_bg"], **kwargs)
        self._api_key = _read_api_key()
        self._setup_ui()
        self._fetch()

    # ------------------------------------------------------------------
    # UI skeleton
    # ------------------------------------------------------------------
    def _setup_ui(self):
        # Title
        tk.Label(
            self, text="WEATHER", bg=COLORS["panel_bg"],
            fg=COLORS["text_head"], font=(F, 10, "bold"), pady=5
        ).pack()
        tk.Frame(self, bg=COLORS["sep"], height=1).pack(fill="x", padx=6)

        # TODAY block
        self._today_frame = tk.Frame(self, bg=COLORS["panel_bg"])
        self._today_frame.pack(fill="x", padx=10, pady=(6, 2))

        tk.Label(
            self._today_frame, text="TODAY", bg=COLORS["panel_bg"],
            fg=COLORS["accent"], font=(F, 8, "bold")
        ).pack(anchor="w")

        self._t_icon  = self._big_lbl(self._today_frame, "–",  24)
        self._t_temp  = self._big_lbl(self._today_frame, "– °F", 14)
        self._t_desc  = self._small_lbl(self._today_frame, "–")
        self._t_extra = self._small_lbl(self._today_frame, "")

        tk.Frame(self, bg=COLORS["sep"], height=1).pack(fill="x", padx=6, pady=(4, 0))

        # TOMORROW block
        self._tmrw_frame = tk.Frame(self, bg=COLORS["panel_bg"])
        self._tmrw_frame.pack(fill="x", padx=10, pady=(6, 2))

        tk.Label(
            self._tmrw_frame, text="TOMORROW", bg=COLORS["panel_bg"],
            fg=COLORS["accent"], font=(F, 8, "bold")
        ).pack(anchor="w")

        self._m_icon  = self._big_lbl(self._tmrw_frame, "–",  20)
        self._m_temp  = self._big_lbl(self._tmrw_frame, "– °F", 12)
        self._m_desc  = self._small_lbl(self._tmrw_frame, "")
        self._m_extra = self._small_lbl(self._tmrw_frame, "")

        # Last-updated label at bottom
        self._updated_var = tk.StringVar(value="")
        tk.Label(
            self, textvariable=self._updated_var,
            bg=COLORS["panel_bg"], fg=COLORS["text_dim"], font=(F, 7)
        ).pack(side="bottom", pady=2)

    def _big_lbl(self, parent, text, size):
        lbl = tk.Label(
            parent, text=text, bg=COLORS["panel_bg"],
            fg=COLORS["text_bright"], font=(F, size, "bold")
        )
        lbl.pack()
        return lbl

    def _small_lbl(self, parent, text):
        lbl = tk.Label(
            parent, text=text, bg=COLORS["panel_bg"],
            fg=COLORS["text_dim"], font=(F, 8)
        )
        lbl.pack()
        return lbl

    # ------------------------------------------------------------------
    # Fetch logic
    # ------------------------------------------------------------------
    def _fetch(self):
        if not self._api_key:
            self._t_icon.config(text="!")
            self._t_temp.config(text="No API key")
            self._t_desc.config(text="Add OPENWEATHER_API_KEY")
            self._t_extra.config(text="to .env file")
            self.after(60_000, self._fetch)
            return
        if not HAS_REQUESTS:
            self._t_desc.config(text="requests not installed")
            return
        threading.Thread(target=self._fetch_thread, daemon=True).start()
        self.after(WEATHER_REFRESH_MIN * 60 * 1000, self._fetch)

    def _fetch_thread(self):
        try:
            base = "https://api.openweathermap.org/data/2.5"
            params = {"q": WEATHER_CITY, "appid": self._api_key, "units": WEATHER_UNITS}

            current  = requests.get(f"{base}/weather",  params=params, timeout=10).json()
            forecast = requests.get(f"{base}/forecast", params=params, timeout=10).json()

            self.after(0, lambda: self._update_ui(current, forecast))
        except Exception:
            self.after(0, lambda: self._t_desc.config(text="Network error"))

    def _update_ui(self, current, forecast):
        # ── Today ──────────────────────────────────────────────────────
        main    = current.get("main", {})
        weather = current.get("weather", [{}])[0]
        cond    = weather.get("main", "Clear")

        self._t_icon.config(text=ICONS.get(cond, "?"))
        self._t_temp.config(text=f"{int(main.get('temp', 0))}°F")
        self._t_desc.config(text=weather.get("description", "").title())
        hi  = int(main.get("temp_max", 0))
        lo  = int(main.get("temp_min", 0))
        hum = main.get("humidity", 0)
        self._t_extra.config(text=f"H:{hi}° L:{lo}°  hum:{hum}%")

        # ── Tomorrow (from 3-h forecast) ───────────────────────────────
        tmrw    = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        entries = [e for e in forecast.get("list", []) if e.get("dt_txt", "").startswith(tmrw)]

        if entries:
            noon = min(entries, key=lambda e: abs(int(e["dt_txt"][11:13]) - 12))
            cond2 = noon.get("weather", [{}])[0].get("main", "Clear")
            desc2 = noon.get("weather", [{}])[0].get("description", "").title()
            all_hi = [e["main"]["temp_max"] for e in entries]
            all_lo = [e["main"]["temp_min"] for e in entries]
            avg    = sum(e["main"]["temp"] for e in entries) / len(entries)

            self._m_icon.config(text=ICONS.get(cond2, "?"))
            self._m_temp.config(text=f"{int(avg)}°F avg")
            self._m_desc.config(text=desc2)
            self._m_extra.config(text=f"H:{int(max(all_hi))}° L:{int(min(all_lo))}°")

        now_str = datetime.datetime.now().strftime("%H:%M")
        self._updated_var.set(f"updated {now_str}")
