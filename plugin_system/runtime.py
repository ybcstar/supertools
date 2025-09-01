import logging, threading, functools, traceback
from plugin_system.container import Container

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def safe_run(plugin_cls, root, ctx):
    try:
        inst = plugin_cls(root)
        inst.run(ctx)
    except Exception as e:
        logging.exception("plugin crash")
        import ttkbootstrap as tb
        tb.dialogs.Messagebox.show_error(f"{e}", "插件异常")

def daemon_thread(target):
    t = threading.Thread(target=target, daemon=True)
    t.start()
    return t