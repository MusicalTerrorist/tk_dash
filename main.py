import tkinter as tk
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import COLORS
from widgets.top_bar  import TopBar
from widgets.weather  import WeatherPanel
from widgets.tracker  import TrackerPanel
from widgets.pomodoro import PomodoroPanel
from widgets.photo    import PhotoPanel


def _panel(parent, **kwargs):
    """Convenience: styled panel frame with retro border."""
    return tk.Frame(
        parent,
        bg=COLORS["panel_bg"],
        highlightbackground=COLORS["border"],
        highlightthickness=1,
        **kwargs,
    )


def main():
    root = tk.Tk()
    root.title("Daily Dashboard")
    root.configure(bg=COLORS["bg"])

    # ── Fullscreen ───────────────────────────────────────────────────────
    # root.attributes("-fullscreen", True)
    root.geometry("800x480")
    root.bind("<Escape>", lambda e: root.destroy())   # Esc to quit (dev)

    # ── Top bar (fixed height, full width) ──────────────────────────────
    TopBar(root).pack(side="top", fill="x")

    # ── Content area ────────────────────────────────────────────────────
    content = tk.Frame(root, bg=COLORS["bg"])
    content.pack(fill="both", expand=True)

    # Column weights: left=1  center=2  right=1  → 25% / 50% / 25%
    content.grid_columnconfigure(0, weight=1, minsize=150)
    content.grid_columnconfigure(1, weight=2, minsize=200)
    content.grid_columnconfigure(2, weight=1, minsize=150)
    content.grid_rowconfigure(0, weight=1)

    # ── Left: Weather ───────────────────────────────────────────────────
    left = _panel(content)
    left.grid(row=0, column=0, sticky="nsew", padx=(3, 1), pady=3)
    WeatherPanel(left).pack(fill="both", expand=True)

    # ── Center column ───────────────────────────────────────────────────
    center = tk.Frame(content, bg=COLORS["bg"])
    center.grid(row=0, column=1, sticky="nsew", padx=1, pady=3)
    center.grid_rowconfigure(0, weight=3)   # tracker  ~ 60 %
    center.grid_rowconfigure(1, weight=2)   # pomodoro ~ 40 %
    center.grid_columnconfigure(0, weight=1)

    # Center-top: Daily tracker
    c_top = _panel(center)
    c_top.grid(row=0, column=0, sticky="nsew", pady=(0, 2))
    TrackerPanel(c_top).pack(fill="both", expand=True)

    # Center-bottom: Pomodoro timer
    c_bot = _panel(center)
    c_bot.grid(row=1, column=0, sticky="nsew", pady=(2, 0))
    PomodoroPanel(c_bot).pack(fill="both", expand=True)

    # ── Right: Photo gallery ────────────────────────────────────────────
    right = _panel(content)
    right.grid(row=0, column=2, sticky="nsew", padx=(1, 3), pady=3)
    PhotoPanel(right).pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
