# desktop/main.py
import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("CircleSync")

# Starting Fullscreen
try:
    root.state("zoomed")
except Exception:
    pass

# Page background
root.grid_rowconfigure(0, weight = 1)
root.grid_columnconfigure(0, weight = 1)
page = ttk.Frame(root, padding = 12)
page.grid(row = 0, column = 0, sticky = "nsew")

# Make a 3x3 grid. 
for r in range(3):
    page.grid_rowconfigure(r, weight = 1)

# Center cell (1,1) will hold the card
for c in range(3):
    page.grid_columnconfigure(c, weight = 1)

# Centered card
card = ttk.Frame(page, padding = 20, relief = "ridge")

# Center
card.grid(row = 1, column = 1)

ttk.Label(card, text = "Create a CircleSync account", font = ("Segoe UI", 14, "bold")).grid(row = 0, column = 0, columnspan = 2, pady = (0, 12))

ttk.Button(card, text="Create an account", command = lambda: messagebox.showinfo("Create", "Create account (placeholder)")).grid(row = 1, column = 0, columnspan = 2, sticky = "ew", pady = (0, 10))

ttk.Label(card, text = "or").grid(row = 2, column = 0, columnspan = 2, pady = (0, 8))

email_var = tk.StringVar()
passwd_var = tk.StringVar()
show_passwd = tk.BooleanVar(value = False)

# Email or Username
ttk.Label(card, text = "Username / Email").grid(row = 3, column = 0, sticky = "w", pady = 4)
ttk.Entry(card, textvariable = email_var, width = 32).grid(row = 3, column = 1, pady = 4)

# Password
ttk.Label(card, text = "Password").grid(row = 4, column = 0, sticky = "w", pady = 4)

# Single password entry
passwd_entry = ttk.Entry(card, textvariable = passwd_var, show = "•", width = 32)
passwd_entry.grid(row = 4, column = 1, pady = 4)
def toggle_password():
    passwd_entry.configure(show = "" if show_passwd.get() else "•")

# Show Password checkbox
tk.Checkbutton(card, text = "Show password", variable = show_passwd, command = toggle_password).grid(row = 5, column = 0, columnspan = 2, sticky = "w")

def on_login():
    u, p = email_var.get().strip(), passwd_var.get().strip()
    if not u or not p:
        messagebox.showwarning("Missing info", "Please enter both username/email and password.")
        return
    messagebox.showinfo("Login", f"(mock) Logging in as {u}")

# Login Button
ttk.Button(card, text = "Log In", command = on_login).grid(row = 6, column = 0, columnspan = 2, sticky = "ew", pady = (10, 0))

# Make inputs stretch nicely inside the card
for col in range(2):
    card.grid_columnconfigure(col, weight = 1)

root.bind("<Return>", lambda e: on_login())

root.mainloop()