import tkinter as tk

from config import COLORS, F, POMODORO_WORK_MIN, POMODORO_BREAK_MIN


class PomodoroPanel(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["panel_bg"], **kwargs)
        self._work_sec  = POMODORO_WORK_MIN  * 60
        self._break_sec = POMODORO_BREAK_MIN * 60
        self._time_left = self._work_sec
        self._mode      = "work"   # "work" | "break"
        self._running   = False
        self._sessions  = 0
        self._after_id  = None
        self._build()

    # ------------------------------------------------------------------
    # Build UI
    # ------------------------------------------------------------------
    def _build(self):
        # Title row + session checkmarks
        top = tk.Frame(self, bg=COLORS["panel_bg"])
        top.pack(fill="x", padx=8, pady=(4, 0))

        tk.Label(
            top, text="FOCUS TIMER",
            bg=COLORS["panel_bg"], fg=COLORS["text_head"], font=(F, 10, "bold")
        ).pack(side="left")

        self._marks_frame = tk.Frame(top, bg=COLORS["panel_bg"])
        self._marks_frame.pack(side="right")

        tk.Frame(self, bg=COLORS["sep"], height=1).pack(fill="x", padx=6, pady=(2, 0))

        # Body: large timer on left, controls on right
        body = tk.Frame(self, bg=COLORS["panel_bg"])
        body.pack(fill="both", expand=True, padx=6, pady=4)

        # ── Timer display ───────────────────────────────────────────────
        left = tk.Frame(body, bg=COLORS["panel_bg"])
        left.pack(side="left", fill="both", expand=True)

        self._time_var = tk.StringVar(value=self._fmt(self._work_sec))
        self._timer_lbl = tk.Label(
            left, textvariable=self._time_var,
            bg=COLORS["panel_bg"], fg=COLORS["timer_work"],
            font=(F, 30, "bold")
        )
        self._timer_lbl.pack(anchor="center", pady=(4, 0))

        self._mode_var = tk.StringVar(value="WORK  25:00")
        tk.Label(
            left, textvariable=self._mode_var,
            bg=COLORS["panel_bg"], fg=COLORS["text_dim"], font=(F, 8)
        ).pack(anchor="center")

        # ── Buttons ─────────────────────────────────────────────────────
        btn_row = tk.Frame(left, bg=COLORS["panel_bg"])
        btn_row.pack(anchor="center", pady=(4, 0))

        self._start_btn = tk.Button(
            btn_row, text="START", width=8,
            bg=COLORS["btn_bg"], fg=COLORS["success"],
            font=(F, 9, "bold"),
            activebackground=COLORS["btn_active"], activeforeground=COLORS["success"],
            relief="flat", bd=0, pady=3,
            command=self._toggle
        )
        self._start_btn.pack(side="left", padx=(0, 6))

        tk.Button(
            btn_row, text="RESET", width=7,
            bg=COLORS["btn_bg"], fg=COLORS["text_dim"],
            font=(F, 9),
            activebackground=COLORS["btn_active"], activeforeground=COLORS["text"],
            relief="flat", bd=0, pady=3,
            command=self._reset
        ).pack(side="left")

        self._update_marks()

    # ------------------------------------------------------------------
    # Time formatting
    # ------------------------------------------------------------------
    def _fmt(self, seconds):
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    # ------------------------------------------------------------------
    # Controls
    # ------------------------------------------------------------------
    def _toggle(self):
        if self._running:
            self._running = False
            self._start_btn.config(text="RESUME")
            if self._after_id:
                self.after_cancel(self._after_id)
        else:
            self._running = True
            self._start_btn.config(text="PAUSE ")
            self._tick()

    def _reset(self):
        self._running = False
        self._start_btn.config(text="START")
        if self._after_id:
            self.after_cancel(self._after_id)
        self._mode      = "work"
        self._time_left = self._work_sec
        self._time_var.set(self._fmt(self._work_sec))
        self._mode_var.set(f"WORK  {POMODORO_WORK_MIN}:00")
        self._timer_lbl.config(fg=COLORS["timer_work"])

    # ------------------------------------------------------------------
    # Tick
    # ------------------------------------------------------------------
    def _tick(self):
        if not self._running:
            return
        self._time_left -= 1
        self._time_var.set(self._fmt(self._time_left))
        if self._time_left <= 0:
            self._on_complete()
        else:
            self._after_id = self.after(1000, self._tick)

    def _on_complete(self):
        self._running = False
        self._start_btn.config(text="START")

        if self._mode == "work":
            self._sessions += 1
            self._update_marks()
            self._mode      = "break"
            self._time_left = self._break_sec
            self._mode_var.set(f"BREAK  {POMODORO_BREAK_MIN}:00")
            self._timer_lbl.config(fg=COLORS["timer_break"])
        else:
            self._mode      = "work"
            self._time_left = self._work_sec
            self._mode_var.set(f"WORK  {POMODORO_WORK_MIN}:00")
            self._timer_lbl.config(fg=COLORS["timer_work"])

        self._time_var.set(self._fmt(self._time_left))

    # ------------------------------------------------------------------
    # Session checkmarks
    # ------------------------------------------------------------------
    def _update_marks(self):
        for w in self._marks_frame.winfo_children():
            w.destroy()
        for _ in range(self._sessions):
            tk.Label(
                self._marks_frame, text="✓",
                bg=COLORS["panel_bg"], fg=COLORS["success"],
                font=(F, 10, "bold")
            ).pack(side="left", padx=1)
