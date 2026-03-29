import tkinter as tk
import os
import glob as _glob

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from config import COLORS, F, PHOTOS_DIR, PHOTO_CYCLE_MIN

IMAGE_EXTS = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif",
              "*.JPG", "*.JPEG", "*.PNG", "*.BMP", "*.GIF")


class PhotoPanel(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["panel_bg"], **kwargs)
        self._photos    = []
        self._idx       = 0
        self._photo_ref = None
        self._build()
        self._load_photos()
        # Delay first cycle so the window is fully rendered before we read widget dimensions
        self.after(300, self._cycle)

    # ------------------------------------------------------------------
    # Build UI
    # ------------------------------------------------------------------
    def _build(self):
        tk.Label(
            self, text="GALLERY",
            bg=COLORS["panel_bg"], fg=COLORS["text_head"],
            font=(F, 10, "bold"), pady=5
        ).pack()
        tk.Frame(self, bg=COLORS["sep"], height=1).pack(fill="x", padx=6)

        self._img_lbl = tk.Label(
            self, bg=COLORS["panel_bg"],
            fg=COLORS["text_dim"], font=(F, 9)
        )
        self._img_lbl.pack(fill="both", expand=True, padx=4, pady=4)

    # ------------------------------------------------------------------
    # Load file list
    # ------------------------------------------------------------------
    def _load_photos(self):
        if not HAS_PIL:
            self._img_lbl.config(text="Pillow not\ninstalled")
            return
        files = []
        for ext in IMAGE_EXTS:
            files.extend(_glob.glob(os.path.join(PHOTOS_DIR, ext)))
        self._photos = sorted(set(files))
        if not self._photos:
            self._img_lbl.config(text="No photos in\nassets/photos/")

    # ------------------------------------------------------------------
    # Cycling
    # ------------------------------------------------------------------
    def _cycle(self):
        if self._photos and HAS_PIL:
            self._show(self._idx)
            self._idx = (self._idx + 1) % len(self._photos)
        self.after(PHOTO_CYCLE_MIN * 60 * 1000, self._cycle)

    def _show(self, idx):
        try:
            self.update_idletasks()
            w = max(self._img_lbl.winfo_width(),  10)
            h = max(self._img_lbl.winfo_height(), 10)

            img = Image.open(self._photos[idx]).convert("RGBA")
            img.thumbnail((w, h), Image.LANCZOS)

            self._photo_ref = ImageTk.PhotoImage(img)
            self._img_lbl.config(image=self._photo_ref, text="")
        except Exception:
            self._img_lbl.config(text="Error loading\nphoto", image="")
            self._photo_ref = None
