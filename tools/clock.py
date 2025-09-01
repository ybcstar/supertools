import datetime, ttkbootstrap as tb
from plugin_system.plugin import Plugin
from plugin_system.helpers import newWindow

class ClockPlugin(Plugin):
    name = "实时时钟"

    def __init__(self, root):  # ← 加 root
        super().__init__(root)

    def run(self, ctx):
        win = newWindow("实时时钟", "220x80")
        lbl = tb.Label(win, font=("Segoe UI", 32), anchor="center")
        lbl.pack(fill="both", expand=True)

        def tick():
            if win.winfo_exists():
                lbl.configure(text=datetime.datetime.now().strftime("%H:%M:%S"))
                win.after(200, tick)
        tick()