#!/usr/bin/env python3
import pathlib, json, logging, traceback,ttkbootstrap as tb
from plugin_system.container import Container
from plugin_system.scanner import scan
from plugin_system.skin_adapter import SkinAdapter
from plugin_system.helpers import is_admin
from plugin_system.network import NetService
from plugin_system.runtime import safe_run, daemon_thread

logging.basicConfig(level=logging.INFO)


ROOT = pathlib.Path(__file__).parent
CONFIG_FILE = ROOT / "config.json"

# 扫描所有插件
PLUGINS = {}
for d in (ROOT / "plugins", ROOT / "tools"):
    PLUGINS.update(scan(d))

# 过滤可见插件
VISIBLE = {k: v for k, v in PLUGINS.items()
           if not (hasattr(v, "visible") and not v.visible())}

# 读/写配置
if not CONFIG_FILE.exists():
    CONFIG_FILE.write_text(json.dumps({"skin": "default"}))
cfg = json.loads(CONFIG_FILE.read_text())

class App(tb.Window):
    def __init__(self):
        super().__init__("Supertools", minsize=(600, 450))
        Container.register("root", self)
        self.skin = SkinAdapter(self, cfg["skin"])

        # 顶部标题 + 皮肤切换
        top = tb.Frame(self)
        top.pack(fill="x", pady=5)
        tb.Label(top, text="Supertools", font=("Segoe UI", 24)).pack(side="left", padx=20)
        self.skin_var = tb.StringVar(value=cfg["skin"])
        cb = tb.Combobox(top, textvariable=self.skin_var,
                         values=["default", "dark", "light", "cyber"],
                         state="readonly", width=10)
        cb.pack(side="right", padx=10)
        cb.bind("<<ComboboxSelected>>", self.change_skin)

        # 网格工具区
        self.grid_frame = tb.Frame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.render_grid()

    def change_skin(self, _):
        new_skin = self.skin_var.get()
        self.skin = SkinAdapter(self, new_skin)
        cfg["skin"] = new_skin
        CONFIG_FILE.write_text(json.dumps(cfg))

    def render_grid(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        COLS = 2
        for idx, (_, cls) in enumerate(VISIBLE.items()):
            card = tb.Frame(self.grid_frame)
            tb.Label(card, text=cls(None).name, font=("Segoe UI", 14)).pack(pady=5)
            tb.Button(card, text="打开",
                      command=lambda c=cls: self.safe_run(c,self),
                      style="primary-outline").pack()
            card.grid(row=idx // COLS, column=idx % COLS,
                      padx=10, pady=10, sticky="nsew")
        for c in range(COLS):
            self.grid_frame.columnconfigure(c, weight=1)

    @staticmethod
    def safe_run(plugin_cls, root):
        try:
            inst = plugin_cls(root)
            inst.run(Container)
        except Exception:
            tb.dialogs.Messagebox.show_error(traceback.format_exc(), "插件异常")

    def run_plugin(self, cls):
        try:
            self.safe_run(cls, self)
        except Exception as e:
            tb.dialogs.Messagebox.show_error(str(e), "插件异常")

if __name__ == "__main__":
    App().mainloop()