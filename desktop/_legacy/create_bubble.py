import tkinter as tk
from tkinter import ttk, messagebox

def _centered_card(parent):
    for r in range(3):
        parent.grid_rowconfigure(r, weight = 1)
    for c in range(3):
        parent.grid_columnconfigure(c, weight = 1)
    card = ttk.Frame(parent, padding = 20, relief = "ridge")
    card.grid(row = 1, column = 1)
    return card

class CreateBubbleScreen(ttk.Frame):
    """Simple placeholder for creating an Interest Bubble."""
    def __init__(self, parent, show_callback):
        super().__init__(parent, padding=12)
        self.show = show_callback

        card = _centered_card(self)

        ttk.Label(card, text = "Create Bubble", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan = 2, pady = (0,12))

        name = tk.StringVar()
        rules = tk.StringVar()

        ttk.Label(card, text = "Bubble Name").grid(row = 1, column = 0, sticky = "w", pady = 4)
        ttk.Entry(card, textvariable = name, width = 32).grid(row = 1, column = 1, pady = 4)

        ttk.Label(card, text = "Rules (optional)").grid(row = 2, column = 0, sticky = "w", pady = 4)
        ttk.Entry(card, textvariable = rules, width = 32).grid(row = 2, column = 1, pady = 4)

        btns = ttk.Frame(card)
        btns.grid(row = 3, column = 0, columnspan = 2, pady = 10, sticky = "ew")
        ttk.Button(btns, text = "Back", command = lambda: self.show("feed")).pack(side = "left")
        ttk.Button(btns, text = "Create", command = lambda: messagebox.showinfo("Bubble", "(mock) Bubble created")).pack(side = "right")

        for c in range(2):
            card.grid_columnconfigure(c, weight=1)
