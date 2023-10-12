import tkinter as tk

from _version import __version__
from GUI.Controllers import MainController

# Better readability (prevents blurry text) on high DPI displays
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title(f"KismetDB2KML {__version__}")
    app = MainController(root)
    root.mainloop()