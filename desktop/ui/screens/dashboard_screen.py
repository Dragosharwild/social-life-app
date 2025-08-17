import tkinter as tk
from tkinter import ttk

from services.circle_service import CircleService


MOCK_INTERESTS = [
	{"id": 1, "name": "Sports"},
	{"id": 2, "name": "Tech"},
	{"id": 3, "name": "Music"},
	{"id": 4, "name": "Art"},
	{"id": 5, "name": "Gaming"},
	{"id": 6, "name": "Books"},
	{"id": 7, "name": "Movies"},
	{"id": 8, "name": "Fitness"},
	{"id": 9, "name": "Food"},
	{"id": 10, "name": "Travel"},
]


def _centered_card(parent):
	for r in range(3):
		parent.grid_rowconfigure(r, weight=1)
	for c in range(3):
		parent.grid_columnconfigure(c, weight=1)
	card = ttk.Frame(parent, padding=20, relief="ridge")
	card.grid(row=1, column=1)
	return card


class DashboardScreen(ttk.Frame):
	def __init__(self, parent, show_callback, circles: CircleService):
		super().__init__(parent)
		self.show = show_callback
		self.circles = circles
		self.followed = set()

		# Center the card in the whole screen
		card = _centered_card(self)

		ttk.Label(card, text="Pick your interests", font=("Segoe UI", 14, "bold")).grid(
			row=0, column=0, columnspan=3, pady=(0, 12)
		)

		self.query = tk.StringVar()
		search_entry = ttk.Entry(card, textvariable=self.query, width=30)
		search_entry.grid(row=1, column=0, columnspan=3, pady=(0, 12))
		search_entry.bind("<KeyRelease>", lambda e: self.refresh())

		self.grid_frame = ttk.Frame(card)
		self.grid_frame.grid(row=2, column=0, columnspan=3)

		self.refresh()

		ttk.Button(card, text="Log out", command=lambda: self.show("login")).grid(
			row=3, column=0, sticky="w", pady=(12, 0)
		)
		ttk.Button(card, text="Continue", command=lambda: self.show("feed")).grid(
			row=3, column=2, sticky="e", pady=(12, 0)
		)

		for col in range(3):
			card.grid_columnconfigure(col, weight=1)

	def refresh(self):
		# Clear old items
		for widget in self.grid_frame.winfo_children():
			widget.destroy()

		# Filter
		q = self.query.get().lower()
		items = [i for i in MOCK_INTERESTS if q in i["name"].lower()]

		# Draw interests in a grid
		cols = 3
		for idx, item in enumerate(items):
			r, c = divmod(idx, cols)
			frame = ttk.Frame(self.grid_frame, padding=10, relief="groove")
			frame.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

			ttk.Label(frame, text=item["name"]).pack()
			btn_text = "Unfollow" if item["id"] in self.followed else "Follow"
			ttk.Button(
				frame, text=btn_text, command=lambda it=item: self._toggle_follow(it["id"])  # noqa: B023
			).pack(pady=(5, 0))

		for c in range(cols):
			self.grid_frame.grid_columnconfigure(c, weight=1)

	def _toggle_follow(self, interest_id):
		if interest_id in self.followed:
			self.followed.remove(interest_id)
		else:
			self.followed.add(interest_id)
		self.refresh()

