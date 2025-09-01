import ttkbootstrap as tb
import math

class RichTextLabel(tb.Text):
    def __init__(self, parent, **kw):
        super().__init__(parent, wrap="word", state="disabled", height=8, **kw)
        from tkinter.font import Font
        self.tag_configure("red", foreground="#ff5555")
        self.tag_configure("big", font=Font(size=14, weight="bold"))

    def append(self, text, tags=None):
        self.configure(state="normal")
        self.insert("end", text, tags or ())
        self.configure(state="disabled")
        self.see("end")

class InputBox(tb.Frame):
    def __init__(self, parent, label="", **kw):
        super().__init__(parent)
        if label:
            tb.Label(self, text=label).pack(anchor="w")
        self.entry = tb.Entry(self, **kw)
        self.entry.pack(fill="x", pady=2)

    def get(self): return self.entry.get()
    def set(self, val):
        self.entry.delete(0, "end")
        self.entry.insert(0, val)

class Button(tb.Button):
    def __init__(self, parent, text, on_click=None, **kw):
        super().__init__(parent, text=text, **kw)
        if on_click:
            self.configure(command=on_click)

class Bar(tb.Frame):
    def __init__(self, parent, orient="horizontal", length=200, **kw):
        super().__init__(parent)
        style = "info" if orient == "horizontal" else "warning"
        self.pb = tb.Progressbar(self, orient=orient, maximum=100, length=length,
                                 style=f"{style}.TProgressbar", **kw)
        self.pb.pack(fill="x" if orient == "horizontal" else "y")

    def set_value(self, v):
        self.pb.configure(value=max(0, min(100, int(v))))

class Geometry(tb.Canvas):
    def __init__(self, parent, **kw):
        super().__init__(parent, highlightthickness=0, bg="#1e1e2e", **kw)
        self.bind("<Configure>", self._on_resize)

    def draw_polygon(self, points, fill="#448aff", outline="#ffffff"):
        self._pts = points
        self._style = dict(fill=fill, outline=outline, width=2)
        self.redraw()

    def redraw(self):
        self.delete("poly")
        if not getattr(self, "_pts", None):
            return
        w, h = self.winfo_width(), self.winfo_height()
        if w < 2 or h < 2:
            return
        coords = [((x + 1) * w / 2, (1 - y) * h / 2) for x, y in self._pts]
        self.create_polygon(*coords, tag="poly", **self._style)

    def _on_resize(self, _):
        self.redraw()