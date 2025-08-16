from tkinter import ttk, messagebox

from services.circle_service import CircleService


def _centered_card(parent):
	for r in range(3):
		parent.grid_rowconfigure(r, weight=1)
	for c in range(3):
		parent.grid_columnconfigure(c, weight=1)
	card = ttk.Frame(parent, padding=20, relief="ridge")
	card.grid(row=1, column=1)
	return card


class BubbleDetailScreen(ttk.Frame):
	"""Simple details screen with placeholder join/leave actions."""

	def __init__(self, parent, show_callback, circles: CircleService):
		super().__init__(parent, padding=12)
		self.show = show_callback
		self.circles = circles

		card = _centered_card(self)
		ttk.Label(card, text="Circle Details", font=("Segoe UI", 14, "bold")).grid(
			row=0, column=0, columnspan=2, pady=(0, 12)
		)

		ttk.Label(card, text="Creator: (mock)").grid(row=1, column=0, sticky="w", pady=4)
		ttk.Label(card, text="Members: (mock)").grid(row=2, column=0, sticky="w", pady=4)

		btns = ttk.Frame(card)
		btns.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
		ttk.Button(btns, text="Back", command=lambda: self.show("dashboard")).pack(side="left")
		ttk.Button(btns, text="Create Bubble", command=lambda: messagebox.showinfo("Bubble", "(mock) Bubble created")).pack(
			side="right"
		)

		for c in range(2):
			card.grid_columnconfigure(c, weight=1)

