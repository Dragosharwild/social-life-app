from tkinter import ttk

from ui.widgets.sidebar import Sidebar


def _centered_card(parent):
    for r in range(3):
        parent.grid_rowconfigure(r, weight=1)
    for c in range(3):
        parent.grid_columnconfigure(c, weight=1)
    card = ttk.Frame(parent, padding=20, relief="ridge")
    card.grid(row=1, column=1)
    return card


class ProfileScreen(ttk.Frame):
    """Placeholder profile screen, now with a persistent sidebar."""

    def __init__(self, parent, show_callback):
        super().__init__(parent, padding=12)
        self.show = show_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Main content
        main = ttk.Frame(self)
        main.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        card = _centered_card(main)
        ttk.Label(card, text="Profile", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 12)
        )
        ttk.Label(card, text="Username: demo_user").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Label(card, text="Created Bubbles: (mock)").grid(row=2, column=0, sticky="w", pady=4)

        # Sidebar
        Sidebar(self, self.show).grid(row=0, column=1, sticky="ns")
