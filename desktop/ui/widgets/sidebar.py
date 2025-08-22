from tkinter import ttk


class Sidebar(ttk.Frame):
    """Right-side navigation used across Feed/Create/Profile screens.

    Keeps nav consistent and easy to extend.
    """

    def __init__(self, parent, show_callback):
        super().__init__(parent, padding=12, relief="ridge")
        self.show = show_callback

        ttk.Label(self, text="Navigate", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        ttk.Button(self, text="Home", command=lambda: self.show("feed")).pack(fill="x", pady=4)
        ttk.Button(self, text="Create Bubble", command=lambda: self.show("create_bubble")).pack(fill="x", pady=4)
        ttk.Button(self, text="Profile", command=lambda: self.show("profile")).pack(fill="x", pady=4)
