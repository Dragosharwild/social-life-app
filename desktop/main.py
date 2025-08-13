import tkinter as tk
from tkinter import ttk, messagebox
from create_account import CreateAccountScreen

root = tk.Tk()
root.title("CircleSync")

# Starting Fullscreen
try:
    root.state("zoomed")
except Exception:
    pass

# Page Background
# Root uses grid only
root.grid_rowconfigure(0, weight = 1)
root.grid_columnconfigure(0, weight = 1)

# Screen manager container
container = ttk.Frame(root)
container.grid(row = 0, column = 0, sticky = "nsew")
# allow child frames to expand
container.grid_rowconfigure(0, weight = 1)
container.grid_columnconfigure(0, weight = 1)

screens = {}

def show(name: str):
    screens[name].tkraise()

# Center a card in a 3x3 grid
def centered_card(parent):
    for r in range(3):
        parent.grid_rowconfigure(r, weight = 1)
    for c in range(3):
        parent.grid_columnconfigure(c, weight = 1)
    card = ttk.Frame(parent, padding=20, relief = "ridge")
    card.grid(row = 1, column = 1)
    return card

# Login screen
login = ttk.Frame(container)
login.grid(row = 0, column = 0, sticky = "nsew")
login.grid_rowconfigure(0, weight = 1)
login.grid_columnconfigure(0, weight = 1)
screens["login"] = login

card = centered_card(login)

ttk.Label(card, text = "Create a CircleSync account", font = ("Segoe UI", 14, "bold")).grid(row = 0, column = 0, columnspan = 2, pady = (0, 12))

ttk.Button(card, text = "Create an account", command = lambda: show("create")).grid(row = 1, column = 0, columnspan = 2, sticky = "ew", pady = (0, 10))

ttk.Label(card, tex = "or").grid(row = 2, column = 0, columnspan = 2, pady = (0, 8))

email_var   = tk.StringVar()
passwd_var  = tk.StringVar()
show_passwd = tk.BooleanVar(value = False)

ttk.Label(card, text="Username / Email").grid(row = 3, column = 0, sticky = "w", pady = 4)
ttk.Entry(card, textvariable = email_var, width = 32).grid(row = 3, column = 1, pady = 4)

ttk.Label(card, text="Password").grid(row = 4, column = 0, sticky = "w", pady = 4)
passwd_entry = ttk.Entry(card, textvariable = passwd_var, show = "•", width = 32)
passwd_entry.grid(row = 4, column = 1, pady = 4)

def toggle_password():
    passwd_entry.configure(show = "" if show_passwd.get() else "•")

ttk.Checkbutton(card, text = "Show password", variable = show_passwd, command = toggle_password).grid(row = 5, column = 0, columnspan = 2, sticky = "w")

def on_login():
    u, p = email_var.get().strip(), passwd_var.get().strip()
    if not u or not p:
        messagebox.showwarning("Missing info", "Please enter both username/email and password.")
        return
    messagebox.showinfo("Login", f"(mock) Logging in as {u}")

ttk.Button(card, text = "Log In", command = on_login).grid(row = 6, column = 0, columnspan = 2, sticky = "ew", pady = (10, 0))

for col in range(2):
    card.grid_columnconfigure(col, weight = 1)

# Create Account screen
create = CreateAccountScreen(container, show_callback = show)
create.grid(row = 0, column = 0, sticky = "nsew")
screens["create"] = create

# Start on login
show("login")

root.mainloop()