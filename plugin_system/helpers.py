import os, sys, ctypes
import ttkbootstrap as tb

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return os.geteuid() == 0

def newWindow(title, size="300x200", on_close=None):
    win = tb.Toplevel()
    win.title(title)
    win.geometry(size)
    win.transient()
    win.protocol("WM_DELETE_WINDOW", lambda: (_close(win, on_close)))
    return win

def _close(win, cb):
    if callable(cb):
        cb()
    win.destroy()