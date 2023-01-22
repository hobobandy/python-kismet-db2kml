# -*- coding: utf-8 -*-

import tkinter as tk

from GUI.Controllers import MainController

# Better readability (prevents blurry text) on high DPI displays
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("KismetDB2KML 2023-01-R1")
    app = MainController(root)
    root.mainloop()