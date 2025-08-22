import tkinter as tk
from tkinter import ttk

from app.config import APP_TITLE
from app.navigation import Navigator
from app.state import AppState
from infra.db import init_db
from infra.repositories import SQLiteAuthRepository, SQLiteCircleRepository
from services.auth_service import AuthService
from services.circle_service import CircleService
from ui.screens.auth_screen import CreateAccountScreen, LoginScreen
from ui.screens.create_bubble_screen import CreateBubbleScreen
from ui.screens.dashboard_screen import DashboardScreen
from ui.screens.feed_screen import FeedScreen
from ui.screens.profile_screen import ProfileScreen

def run():
    init_db()  # ensure table exists before UI starts

    root = tk.Tk()
    root.title(APP_TITLE)

    # Starting Fullscreen
    try:
        root.state("zoomed")
    except Exception:
        pass

    # Page Background
    # Root uses grid only
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Screen manager container
    container = ttk.Frame(root)
    container.grid(row=0, column=0, sticky="nsew")
    # allow child frames to expand
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    nav = Navigator(container)

    # wiring
    auth_repo = SQLiteAuthRepository()
    circle_repo = SQLiteCircleRepository()
    auth = AuthService(auth_repo)
    circles = CircleService(circle_repo)
    # app state
    state = AppState()

    # screens
    login = LoginScreen(container, nav.show, auth, app_state=state, circles_service=circles)
    create = CreateAccountScreen(container, nav.show, auth)
    interests = DashboardScreen(container, nav.show, circles)
    feed = FeedScreen(container, nav.show)
    create_bubble = CreateBubbleScreen(container, nav.show)
    profile = ProfileScreen(container, nav.show)

    for name, frame in (
        ("login", login),
        ("create_account", create),
        ("interests", interests),
        ("feed", feed),
        ("create_bubble", create_bubble),
        ("profile", profile),
    ):
        nav.register(name, frame)

    nav.show("login")
    root.mainloop()
