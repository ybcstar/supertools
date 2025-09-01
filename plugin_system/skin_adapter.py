import ttkbootstrap as tb
from skin import load_skin

class SkinAdapter:
    def __init__(self, root, skin_name="default"):
        self.root = root
        self.data = load_skin(skin_name)
        self.apply()

    def apply(self):
        tb.Style().theme_use(self.data["theme"])
        self.root.configure(bg=self.data["colors"]["bg"])