import tkinter as tk
import os
import datetime

from config import COLORS, F, LOG_FILE

ACTIVITIES = [
    ("study",      "STUDY"),
    ("exercise",   "EXERCISE"),
    ("meditation", "MEDIT."),
]

STEPS = [5, 15, 30]   # quick-add buttons in minutes


class TrackerPanel(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["panel_bg"], **kwargs)
        self._values = {key: 0 for key, _ in ACTIVITIES}
        self._val_labels = {}
        self._status_var = tk.StringVar()
        self._build()

    # ------------------------------------------------------------------
    # Build UI
    # ------------------------------------------------------------------
    def _build(self):
        # Title
        title_row = tk.Frame(self, bg=COLORS["panel_bg"])
        title_row.pack(fill="x", padx=8, pady=(6, 2))
        tk.Label(
            title_row, text="DAILY LOG",
            bg=COLORS["panel_bg"], fg=COLORS["text_head"], font=(F, 10, "bold")
        ).pack(side="left")

        tk.Frame(self, bg=COLORS["sep"], height=1).pack(fill="x", padx=6)

        # Counter rows
        for key, label in ACTIVITIES:
            self._make_row(key, label)

        # Save button + status line
        bottom = tk.Frame(self, bg=COLORS["panel_bg"])
        bottom.pack(fill="x", padx=10, pady=(6, 6))

        tk.Button(
            bottom, text="SAVE LOG",
            bg=COLORS["accent_dim"], fg=COLORS["text_bright"],
            font=(F, 9, "bold"),
            activebackground=COLORS["accent"], activeforeground=COLORS["bg"],
            relief="flat", bd=0, padx=12, pady=4,
            command=self._save
        ).pack(side="left")

        tk.Label(
            bottom, textvariable=self._status_var,
            bg=COLORS["panel_bg"], fg=COLORS["success"], font=(F, 8)
        ).pack(side="left", padx=10)

    def _make_row(self, key, label):
        row = tk.Frame(self, bg=COLORS["panel_bg"])
        row.pack(fill="x", padx=8, pady=3)

        # Activity label (fixed width so columns align)
        tk.Label(
            row, text=label, bg=COLORS["panel_bg"],
            fg=COLORS["text"], font=(F, 9), width=10, anchor="w"
        ).pack(side="left")

        # − button
        tk.Button(
            row, text="−", width=3,
            bg=COLORS["btn_bg"], fg=COLORS["danger"],
            font=(F, 10, "bold"),
            activebackground=COLORS["btn_active"], activeforeground=COLORS["danger"],
            relief="flat", bd=0,
            command=lambda k=key: self._change(k, -5)
        ).pack(side="left", padx=(2, 0))

        # Current value display
        val_lbl = tk.Label(
            row, text="0 min", width=7,
            bg=COLORS["btn_bg"], fg=COLORS["text_bright"],
            font=(F, 10, "bold")
        )
        val_lbl.pack(side="left", padx=2)
        self._val_labels[key] = val_lbl

        # Quick-add step buttons
        for step in STEPS:
            tk.Button(
                row, text=f"+{step}",
                bg=COLORS["btn_bg"], fg=COLORS["accent"],
                font=(F, 8),
                activebackground=COLORS["btn_active"], activeforeground=COLORS["text_bright"],
                relief="flat", bd=0, padx=4, pady=2,
                command=lambda k=key, s=step: self._change(k, s)
            ).pack(side="left", padx=1)

    # ------------------------------------------------------------------
    # Value logic
    # ------------------------------------------------------------------
    def _change(self, key, delta):
        self._values[key] = max(0, self._values[key] + delta)
        self._val_labels[key].config(text=f"{self._values[key]} min")

    # ------------------------------------------------------------------
    # Save to log
    # ------------------------------------------------------------------
    def _save(self):
        try:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            today    = datetime.date.today().strftime("%Y-%m-%d")
            now_time = datetime.datetime.now().strftime("%H:%M")
            entry = (
                f"[{today}  {now_time}]  "
                f"Study: {self._values['study']}min  |  "
                f"Exercise: {self._values['exercise']}min  |  "
                f"Meditation: {self._values['meditation']}min\n"
            )
            with open(LOG_FILE, "a", encoding="utf-8") as fh:
                fh.write(entry)
            self._status_var.set(f"Saved at {now_time}")
            self.after(3000, lambda: self._status_var.set(""))
        except Exception as e:
            self._status_var.set(f"Error: {e}")
