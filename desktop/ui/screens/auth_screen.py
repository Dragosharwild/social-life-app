import tkinter as tk
from tkinter import ttk, messagebox

from services.auth_service import AuthService
from services.circle_service import CircleService
from app.state import AppState


def _centered_card(parent):
	for r in range(3):
		parent.grid_rowconfigure(r, weight=1)
	for c in range(3):
		parent.grid_columnconfigure(c, weight=1)
	card = ttk.Frame(parent, padding=20, relief="ridge")
	card.grid(row=1, column=1)
	return card


class LoginScreen(ttk.Frame):
	"""Minimal login mirroring legacy layout."""

	def __init__(self, parent, show_callback, auth: AuthService, app_state: AppState | None = None, circles_service: CircleService | None = None):
		super().__init__(parent)
		self.show = show_callback
		self.auth = auth
		self.app_state = app_state
		self.circles_service = circles_service

		card = _centered_card(self)

		ttk.Label(card, text="Create a CircleSync account", font=("Segoe UI", 14, "bold")).grid(
			row=0, column=0, columnspan=2, pady=(0, 12)
		)
		ttk.Button(card, text="Create an account", command=lambda: self.show("create_account")).grid(
			row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10)
		)
		ttk.Label(card, text="or").grid(row=2, column=0, columnspan=2, pady=(0, 8))

		self.identifier = tk.StringVar()
		self.password = tk.StringVar()
		self.show_pwd = tk.BooleanVar(value=False)

		ttk.Label(card, text="Username / Email").grid(row=3, column=0, sticky="w", pady=4)
		ttk.Entry(card, textvariable=self.identifier, width=32).grid(row=3, column=1, pady=4)

		ttk.Label(card, text="Password").grid(row=4, column=0, sticky="w", pady=4)
		self.pwd_entry = ttk.Entry(card, textvariable=self.password, show="•", width=32)
		self.pwd_entry.grid(row=4, column=1, pady=4)

		ttk.Checkbutton(
			card, text="Show password", variable=self.show_pwd, command=self._toggle_pw
		).grid(row=5, column=0, columnspan=2, sticky="w")

		ttk.Button(card, text="Log In", command=self._login_clicked).grid(
			row=6, column=0, columnspan=2, sticky="ew", pady=(10, 0)
		)
		ttk.Button(
			card, text="Skip → Interests (dev)", command=lambda: self.show("interests")
		).grid(row=7, column=0, columnspan=2, sticky="ew", pady=(6, 0))

		for col in range(2):
			card.grid_columnconfigure(col, weight=1)

	def _toggle_pw(self):
		self.pwd_entry.configure(show="" if self.show_pwd.get() else "•")

	def _login_clicked(self):
		u, p = self.identifier.get().strip(), self.password.get().strip()
		if not u or not p:
			messagebox.showwarning("Missing info", "Please enter both username/email and password.")
			return
		try:
			user = self.auth.login(u, p)
			if self.app_state is not None:
				self.app_state.current_user = user
			# Conditional routing: new user -> interests; else -> feed
			if self.circles_service and user:
				go_interests = not self.circles_service.user_has_any_memberships(user.id)
				self.show("interests" if go_interests else "feed")
			else:
				self.show("interests")
		except Exception as e:
			messagebox.showerror("Login failed", str(e))


class CreateAccountScreen(ttk.Frame):
	def __init__(self, parent, show_callback, auth: AuthService):
		super().__init__(parent)
		self.show = show_callback
		self.auth = auth
		wrap = _centered_card(self)

		ttk.Label(wrap, text="Create an account", font=("Segoe UI", 14, "bold")).grid(
			row=0, column=0, columnspan=2, pady=(0, 12)
		)

		self.email = tk.StringVar()
		self.username = tk.StringVar()
		self.password = tk.StringVar()
		self.confirm = tk.StringVar()
		self.show_pwd = tk.BooleanVar(value=False)

		ttk.Label(wrap, text="Email").grid(row=1, column=0, sticky="w", pady=4)
		ttk.Entry(wrap, textvariable=self.email, width=35).grid(row=1, column=1, pady=4)

		ttk.Label(wrap, text="New Username").grid(row=2, column=0, sticky="w", padx=4)
		ttk.Entry(wrap, textvariable=self.username, width=35).grid(row=2, column=1, pady=4)

		ttk.Label(wrap, text="New Password").grid(row=3, column=0, sticky="w", pady=4)
		self.pwd_entry = ttk.Entry(wrap, textvariable=self.password, show="•", width=35)
		self.pwd_entry.grid(row=3, column=1, pady=4)

		ttk.Label(wrap, text="Confirm Password").grid(row=4, column=0, sticky="w", pady=4)
		self.conf_entry = ttk.Entry(wrap, textvariable=self.confirm, show="•", width=35)
		self.conf_entry.grid(row=4, column=1, pady=4)

		ttk.Checkbutton(
			wrap, text="Show passwords", variable=self.show_pwd, command=self._toggle_pw
		).grid(row=5, column=0, columnspan=2, sticky="w")

		btns = ttk.Frame(wrap)
		btns.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")
		ttk.Button(btns, text="Back", command=lambda: self.show("login")).pack(side="left")
		ttk.Button(btns, text="Create Account", command=self._create_clicked).pack(side="right")

		for c in range(2):
			wrap.grid_columnconfigure(c, weight=1)

	def _toggle_pw(self):
		show = "" if self.show_pwd.get() else "•"
		self.pwd_entry.configure(show=show)
		self.conf_entry.configure(show=show)

	def _create_clicked(self):
		email = self.email.get().strip()
		username = self.username.get().strip()
		password = self.password.get().strip()
		confirm = self.confirm.get().strip()

		if not all([email, username, password, confirm]):
			messagebox.showwarning("Missing info", "Please fill out all fields.")
			return
		if password != confirm:
			messagebox.showerror("Mismatch", "Passwords do not match.")
			return

		try:
			self.auth.sign_up(email, username, password)
		except Exception as e:
			messagebox.showerror("Unavailable", str(e))
			return

		messagebox.showinfo("Account", "Account created successfully!")
		self.show("login")

