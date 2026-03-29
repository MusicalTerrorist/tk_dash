import tkinter as tk
import os
import random
import datetime

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from config import COLORS, F, AVATARS_DIR, QUOTES_FILE

TOP_HEIGHT = 72  # pixels


class TopBar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["top_bg"], height=TOP_HEIGHT, **kwargs)
        self.pack_propagate(False)
        self._photo_ref = None
        self._build()
        self._update_time()

    # ------------------------------------------------------------------
    # Daily-seeded RNG — same avatar + quote all day, changes at midnight
    # ------------------------------------------------------------------
    def _daily_rng(self):
        seed = int(datetime.date.today().strftime("%Y%m%d"))
        return random.Random(seed)

    def _load_avatar(self):
        if not HAS_PIL:
            return None
        exts = (".png", ".gif", ".bmp", ".jpg", ".jpeg")
        files = [
            f for f in os.listdir(AVATARS_DIR)
            if f.lower().endswith(exts)
        ]
        if not files:
            return None
        chosen = self._daily_rng().choice(files)
        path = os.path.join(AVATARS_DIR, chosen)
        img = Image.open(path).convert("RGBA")
        # Scale pixel art with nearest-neighbour to keep crisp look
        target_h = TOP_HEIGHT - 12
        scale = max(1, target_h // max(img.height, 1))
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
        return ImageTk.PhotoImage(img)

    def _load_quote(self):
        try:
            if not os.path.exists(QUOTES_FILE):
                return "Make today count."
            with open(QUOTES_FILE, "r", encoding="utf-8") as fh:
                lines = [l.strip() for l in fh if l.strip()]
            if not lines:
                return "Make today count."
            return self._daily_rng().choice(lines)
        except Exception:
            return "Make today count."

    # ------------------------------------------------------------------
    # Build UI
    # ------------------------------------------------------------------
    def _build(self):
        # Bottom separator line
        tk.Frame(self, bg=COLORS["accent_dim"], height=1).pack(side="bottom", fill="x")

        # ── Left: avatar ────────────────────────────────────────────────
        left = tk.Frame(self, bg=COLORS["top_bg"])
        left.pack(side="left", padx=(8, 4), pady=4)
        try:
            photo = self._load_avatar()
            if photo:
                self._photo_ref = photo
                tk.Label(left, image=photo, bg=COLORS["top_bg"]).pack()
            else:
                tk.Label(
                    left, text="[?]", bg=COLORS["top_bg"],
                    fg=COLORS["accent"], font=(F, 14, "bold")
                ).pack()
        except Exception:
            tk.Label(
                left, text="[?]", bg=COLORS["top_bg"],
                fg=COLORS["accent"], font=(F, 14, "bold")
            ).pack()

        # ── Right: time + date ──────────────────────────────────────────
        right = tk.Frame(self, bg=COLORS["top_bg"])
        right.pack(side="right", padx=(4, 14), pady=4)

        self._time_var = tk.StringVar()
        tk.Label(
            right, textvariable=self._time_var,
            bg=COLORS["top_bg"], fg=COLORS["text_bright"],
            font=(F, 20, "bold")
        ).pack(anchor="e")

        self._date_var = tk.StringVar()
        tk.Label(
            right, textvariable=self._date_var,
            bg=COLORS["top_bg"], fg=COLORS["text_dim"],
            font=(F, 9)
        ).pack(anchor="e")

        # ── Center: quote ───────────────────────────────────────────────
        center = tk.Frame(self, bg=COLORS["top_bg"])
        center.pack(side="left", fill="both", expand=True, padx=8)

        quote = self._load_quote()
        tk.Label(
            center, text=f'"{quote}"',
            bg=COLORS["top_bg"], fg=COLORS["text"],
            font=(F, 9), wraplength=340, justify="left"
        ).pack(anchor="w", expand=True)

    # ------------------------------------------------------------------
    # Clock — update every second
    # ------------------------------------------------------------------
    def _update_time(self):
        now = datetime.datetime.now()
        self._time_var.set(now.strftime("%H:%M:%S"))
        self._date_var.set(now.strftime("%A, %b %d"))
        self.after(1000, self._update_time)
