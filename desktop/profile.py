import tkinter as tk
from tkinter import ttk

def _centered_card(parent):
    for r in range(3):
        parent.grid_rowconfigure(r, weight = 1)
    for c in range(3):
        parent.grid_columnconfigure(c, weight = 1)
    card = ttk.Frame(parent, padding = 20, relief = "ridge")
    card.grid(row = 1, column = 1)
    return card

class ProfileScreen(ttk.Frame):
    """Simple placeholder profile screen (view created bubbles, etc.)."""
    def __init__(self, parent, show_callback):
        super().__init__(parent, padding = 12)
        self.show = show_callback

        card = _centered_card(self)

        ttk.Label(card, text="Profile", font=("Segoe UI", 14, "bold")).grid(row = 0, column = 0, columnspan = 2, pady = (0,12))

        ttk.Label(card, text="Username: demo_user").grid(row = 1, column = 0, sticky = "w", pady = 4)
        ttk.Label(card, text="Created Bubbles: (mock)").grid(row = 2, column = 0, sticky = "w", pady = 4)

        ttk.Button(card, text="Back to Feed", command=lambda: self.show("feed")).grid(row = 3, column = 0, pady = (12,0), sticky = "w")

        for c in range(2):
            card.grid_columnconfigure(c, weight = 1)
