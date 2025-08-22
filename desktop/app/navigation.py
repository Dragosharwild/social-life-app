from tkinter import ttk
from typing import Dict

class Navigator:
    def __init__(self, container: ttk.Frame):
        self.container = container
        self.screens: Dict[str, ttk.Frame] = {}

    def register(self, name: str, frame: ttk.Frame) -> None:
        frame.grid(row=0, column=0, sticky="nsew")
        self.screens[name] = frame

    def show(self, name: str) -> None:
        self.screens[name].tkraise()
