import tkinter as tk
from tkinter import ttk
from app.view.menu import Menu
from app.view.principal import Principal
from app.controller.control_area import ArquivoController


class App(tk.Tk):
    def __init__(self, titulo):
        super().__init__()
        self.wm_title(titulo)
        self.state('zoomed')
        self.minsize(900,400)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Fundo geral
        self.style.configure("TFrame", background="#ffffff")

        # Labels
        self.style.configure(
            "TLabel",
            background="#ffffff",
            foreground="#000000",
            font=("Segoe UI", 10)
        )

        # Título
        self.style.configure(
            "Title.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground="#000000"
        )

        # Botões do menu
        self.style.configure(
            "Menu.TButton",
            background="#f0f0f0",
            foreground="#000000",
            padding=10,
            relief="flat"
        )

        self.style.map(
            "Menu.TButton",
            background=[("active", "#007acc")],
            foreground=[("active", "#ffffff")]
        )
        
        self.menu = Menu(self)
        self.principal = Principal(self)