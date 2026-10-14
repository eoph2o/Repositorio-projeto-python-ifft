import tkinter as tk
from tkinter import ttk

CHECKED = "☑"
UNCHECKED = "☐"


class CheckTreeview(ttk.Treeview):
    """Treeview com checkbox na coluna #0 e callback ao alternar."""

    def __init__(self, master=None, on_toggle=None, **kw):
        kw.setdefault("show", "tree headings")
        super().__init__(master, **kw)
        self.on_toggle = on_toggle          # função(iid, marcado)
        self.column("#0", width=40, stretch=False, anchor="center")
        self.bind("<Button-1>", self._on_click)
        self.bind("<space>", self._on_space)

    # --- API ---
    def add_item(self, values=(), checked=False, parent="", **kw):
        return self.insert(parent, "end",
                           text=CHECKED if checked else UNCHECKED,
                           values=values, **kw)

    def is_checked(self, iid):
        return self.item(iid, "text") == CHECKED

    def set_checked(self, iid, state, notify=True):
        self.item(iid, text=CHECKED if state else UNCHECKED)
        if notify:
            if self.on_toggle:
                self.on_toggle(iid, state)
            self.event_generate("<<ItemToggled>>")   # evento virtual opcional

    def checked_items(self):
        return [i for i in self.get_children() if self.is_checked(i)]

    # --- eventos internos ---
    def _on_click(self, event):
        # só reage se clicou na célula da coluna #0 (a do checkbox)
        if self.identify_region(event.x, event.y) != "tree":
            return
        if self.identify_column(event.x) != "#0":
            return
        iid = self.identify_row(event.y)
        if iid:
            self.set_checked(iid, not self.is_checked(iid))
            return "break"   # evita mudar a seleção ao clicar no checkbox

    def _on_space(self, event):
        iid = self.focus()
        if iid:
            self.set_checked(iid, not self.is_checked(iid))
            return "break"


# ---------------- exemplo de uso ----------------
def ao_marcar(iid, marcado):
    nome = tree.set(iid, "nome")
    print(f"{nome} -> {'marcado' if marcado else 'desmarcado'}")


root = tk.Tk()
tree = CheckTreeview(root, columns=("nome", "valor"), on_toggle=ao_marcar)
tree.heading("#0", text="")
tree.heading("nome", text="Nome")
tree.heading("valor", text="Valor")
tree.pack(fill="both", expand=True)

for n, v in [("Sinal A", 10), ("Sinal B", 20), ("Sinal C", 30)]:
    tree.add_item(values=(n, v))

# alternativa ao callback: evento virtual
tree.bind("<<ItemToggled>>", lambda e: print("Marcados:", tree.checked_items()))

root.mainloop()