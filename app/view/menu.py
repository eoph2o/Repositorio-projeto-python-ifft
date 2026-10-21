import tkinter as tk
from tkinter import ttk
from app.controller.control_area import Class_ArquivoController
from app.view.principal import Principal
from tkinter import filedialog as fd
from tkinter import messagebox
from io import StringIO
from pathlib import Path


class Menu(ttk.Frame):
    def __init__(self, parent, principal):
        super().__init__(parent, style="TFrame")

        self.principal = principal
        self.arquivos = {}   # nome -> caminho

        self.place(x=0, y=0, relwidth=0.18, relheight=1)

        self.container = ttk.Frame(self)
        self.container.pack(expand=True, fill="both", padx=5, pady=5)

        titulo = ttk.Label(self.container, text="MENU", font=("Segoe UI", 14, "bold"))
        titulo.pack(pady=15)

        btnAbriAq = ttk.Button(self.container, text="Abrir Pasta", style="Menu.TButton", command=self.abrir_pasta)
        btnAbriAq.pack(pady=5, fill="x")
        btnLeTudo = ttk.Button(self.container, text="Ler Todos (loop for)", style="Menu.TButton", command=self.leCalcula)
        btnLeTudo.pack(pady=5, fill="x")

        self.tree = ttk.Treeview(self.container)
        self.tree.pack(expand=True, fill="both", pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def abrir_pasta(self):
        caminho = fd.askdirectory()
        if not caminho:
            return

        arquivoslist = self.manejaArquivo(caminho)
        self.atualizar_lista(arquivoslist)

    def manejaArquivo(self, caminho):
        pasta = Path(caminho)
        self.arquivos = {p.name: str(p) for p in pasta.glob("*.s2p")}
        return list(self.arquivos.keys())

    def atualizar_lista(self, arquivos):
        self.tree.delete(*self.tree.get_children())
        for arq in arquivos:
            self.tree.insert("", "end", text=arq)

    # clique na Treeview -> plota no Principal
    def on_select(self, event):
        item = self.tree.selection()
        if not item:
            return

        nome = self.tree.item(item[0], "text")
        obj = Class_ArquivoController(nome, self.arquivos[nome])
        obj.pegarData()

        real, tempo = obj.get_Fourier()
        freq = obj.get_freq()
        amplitude = obj.get_amplitude()
        fase = obj.get_fase()

        self.principal.plotar(amplitude, fase, freq, real, tempo)

    # botão Ler Todos -> um popup por arquivo
    def leCalcula(self):
        for nome, caminho in self.arquivos.items():
            obj = Class_ArquivoController(nome, caminho)
            obj.pegarData()
            obj.PlotPopUp()