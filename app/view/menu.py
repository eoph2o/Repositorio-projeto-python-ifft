import tkinter as tk
from tkinter import ttk
from app.controller.control_area import ArquivoController
from tkinter import filedialog as fd
from tkinter import messagebox
from io import StringIO
from pathlib import Path



class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame", )

        self.arquivos = {}
        self.listobj = []

        self.place(x=0, y=0, relwidth=0.18, relheight=1)

        self.container = ttk.Frame(self)
        self.container.pack(expand=True, fill="both", padx=5, pady=5)

        titulo = ttk.Label(
            self.container,
            text="MENU",
            font=("Segoe UI", 14, "bold")
        )
        titulo.pack(pady=15)

        btnAbriAq = ttk.Button( self.container, text="Abrir Pasta", style="Menu.TButton", command=self.abrir_pasta )
        btnAbriAq.pack(pady=5, fill="x")
        btnLeTudo = ttk.Button( self.container, text="Ler Todos", style="Menu.TButton", command=self.leCalcula)
        btnLeTudo.pack(pady=5, fill="x")



        self.tree = ttk.Treeview(self.container)
        self.tree.pack(expand=True, fill="both", pady=10)

        # evento de clique
        self.tree.bind("<<TreeviewSelect>>", self.on_select)


    #procurar uma determinada pasta para efetuar a leitura 
    
    def abrir_pasta (self): 
            caminho = fd.askdirectory()
            
            if not caminho:
                return

            arquivoslist = self.manejaArquivo(caminho)

            self.atualizar_lista(arquivoslist)
            
    def atualizar_lista(self, arquivos):
        self.tree.delete(*self.tree.get_children())

        for arq in arquivos:
            self.tree.insert("", "end", text=arq)

    # evento clique 
    def on_select(self, event):
        item = self.tree.selection()

        if not item:  
            return

        nome_arquivo = self.tree.item(item[0], "text")

        #print(f'nome_arquivo: {nome_arquivo}'
        self.ctrl.pegarData(nome_arquivo)
        self.ctrl.get_Fourier()
        self.master.principal.plotar()

    def manejaArquivo(self, caminho):   
        pasta = Path(caminho)

        self.arquivos = {
            p.name: str(p)
            for p in pasta.glob("*.s2p")
        }

        #print(f'Dicionário - arquivos: {self.arquivos}')
        return list(self.arquivos.keys())
            
    def leCalcula(self):
        self.listobj = [
            ArquivoController(nome, caminho)
            for nome, caminho in self.arquivos.items()
    ]

        for obj in self.listobj:
            obj.pegarData()
            obj.PlotPopUp()
            





        
          
        
            