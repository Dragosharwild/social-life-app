import tkinter as tk
from tkinter import ttk

# Mock posts (you can replace with backend data later)
MOCK_POSTS = [
    {"id": 1, "bubble": "Sports", "title": "Grizzies vs Lakers"},
    {"id": 2, "bubble": "Tech",   "title": "Too many AI"},
    {"id": 3, "bubble": "Music",  "title": "New age rappers"},
    {"id": 4, "bubble": "Gaming", "title": "This game sucks"},
    {"id": 5, "bubble": "Food",   "title": "Best taco spots?"},
]

class FeedScreen(ttk.Frame):
    """Phase 3: scrollable feed + right-side nav."""
    def __init__(self, parent, show_callback):
        super().__init__(parent, padding=12)
        self.show = show_callback

        # Main content stretches
        self.grid_columnconfigure(0, weight=1)
        # Sidebar
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # Main content
        main = ttk.Frame(self)
        # space before sidebar
        main.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        header = ttk.Frame(main)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        header.grid_columnconfigure(0, weight=1)
        ttk.Label(header, text="Home Feed", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Button(header, text="Back to Interests", command=lambda: self.show("interests")).grid(row=0, column=1, sticky="e")

        # scrollable posts
        body = ttk.Frame(main)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(body, highlightthickness=0)
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=self.canvas.yview)
        self.post_frame = ttk.Frame(self.canvas, padding=4)

        self.post_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.post_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Render posts
        self.render_posts(MOCK_POSTS)

        # Right sidebar nav
        sidebar = ttk.Frame(self, padding=12, relief="ridge")
        # stick top-to-bottom on the right
        sidebar.grid(row=0, column=1, sticky="ns")

        ttk.Label(sidebar, text="Navigate", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,8))
        ttk.Button(sidebar, text="Home", command=lambda: self.show("feed")).pack(fill="x", pady=4)
        ttk.Button(sidebar, text="Create Bubble", command=lambda: self.show("create_bubble")).pack(fill="x", pady=4)
        ttk.Button(sidebar, text="Profile", command=lambda: self.show("profile")).pack(fill="x", pady=4)

    def render_posts(self, posts):
        for w in self.post_frame.winfo_children():
            w.destroy()
        for p in posts:
            card = ttk.Frame(self.post_frame, padding=10, relief="ridge")
            card.pack(fill="x", pady=6)
            ttk.Label(card, text=p["bubble"], foreground="#666").pack(anchor="w")
            ttk.Label(card, text=p["title"], font=("Segoe UI", 11, "bold")).pack(anchor="w")