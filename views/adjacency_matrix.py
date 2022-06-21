from random import randint
from tkinter import CENTER, END, ttk

from .config import base_padding, bold_font


class ConfigurableAdjacencyMatrix(ttk.Frame):
    def __init__(self, master, n_max):
        super().__init__(master)
        self.adj_matrix = AdjacencyMatrix(self, n_max)
        adj_matrix_config = AdjacencyMatrixTweaks(self, n_max, self.adj_matrix)
        adj_matrix_config.pack(padx=base_padding, pady=base_padding)
        self.adj_matrix.pack(padx=base_padding, pady=base_padding)

    def get_matrix_values(self):
        return self.adj_matrix.get_values()


class AdjacencyMatrixTweaks(ttk.Frame):
    def __init__(self, master, n_max, adj_matrix):
        super().__init__(master)
        self.n_combo = self.NCombobox(
            self, n_max, lambda e: adj_matrix.set_n(self.n_combo.get_val())
        )
        self.n_combo.grid(row=0, column=0, padx=base_padding, pady=base_padding)
        fill_random_btn = ttk.Button(
            self, text="Générer aléa", command=lambda: adj_matrix.fill_random()
        )
        fill_random_btn.grid(row=0, column=1, padx=base_padding, pady=base_padding)
        clear_btn = ttk.Button(self, text="Effacer", command=lambda: adj_matrix.clear())
        clear_btn.grid(row=0, column=2, padx=base_padding, pady=base_padding)

    class NCombobox(ttk.Frame):
        def __init__(self, master, n_max, on_select):
            super().__init__(master)
            label = ttk.Label(self, text="N =")
            label.grid(row=0, column=0, padx=base_padding, pady=base_padding)
            self.combo = ttk.Combobox(
                self,
                values=list(range(2, n_max + 1)),
                width=5,
                state="readonly",
            )
            self.combo.bind("<<ComboboxSelected>>", on_select)
            self.combo.bind("<FocusOut>", lambda e: self.combo.selection_clear())
            self.combo.current(n_max - 2)
            self.combo.grid(row=0, column=1, padx=base_padding, pady=base_padding)

        def get_val(self):
            return int(self.combo.get())


class AdjacencyMatrix(ttk.Frame):
    def __init__(self, master, n_max):
        super().__init__(master)
        self.n_max = n_max
        self.n = n_max
        self.cells = [[0] * n_max for _ in range(n_max)]
        self.error_label = ttk.Label(self, foreground="red")
        self.error_label.grid(row=n_max, column=0, columnspan=n_max, pady=5)

        def validator_wrapper(v, i, j):
            if self._cell_validator(v):
                i, j = int(i), int(j)
                if i != j:
                    self.cells[j][i].config(validate="none")
                    self.cells[j][i].delete(0, END)
                    self.cells[j][i].insert(0, v)
                    self.cells[j][i].config(validate="key")
                self.error_label["text"] = ""
                return True
            self.error_label["text"] = "Veuillez entrer 0 ou 1"
            return False

        vcmd = self.register(validator_wrapper)
        for i in range(n_max):
            for j in range(n_max):
                self.cells[i][j] = ttk.Entry(
                    self,
                    justify=CENTER,
                    width=5,
                    validate="key",
                    validatecommand=(vcmd, "%P", i, j),
                )
                if i == j:
                    self.cells[i][j].insert(0, "0")
                    self.cells[i][j].config(state="disabled")
                self.cells[i][j].grid(row=i, column=j)

    @staticmethod
    def _cell_validator(v):
        if len(v) <= 1:
            if len(v) == 0:
                return True
            v = v[0]
            return v == "0" or v == "1"

    def get_values(self):
        m = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                v = self.cells[i][j].get()
                if v:
                    m[i][j] = int(v)
        return m

    def set_n(self, new_n):
        if new_n > self.n_max:
            new_n = self.n_max
        if new_n <= self.n:
            for i in range(new_n, self.n):
                for j in range(0, self.n):
                    if i != j:
                        self.cells[i][j].delete(0, END)
                        self.cells[i][j].config(state="disabled")
                        self.cells[j][i].delete(0, END)
                        self.cells[j][i].config(state="disabled")
                    else:
                        self.cells[i][i].config(state="normal")
                        self.cells[i][i].delete(0, END)
                        self.cells[i][i].config(state="disabled")
        else:
            for i in range(self.n, new_n):
                for j in range(0, new_n):
                    if i != j:
                        self.cells[i][j].config(state="normal")
                        self.cells[j][i].config(state="normal")
                    else:
                        self.cells[i][i].config(state="normal")
                        self.cells[i][i].insert(0, "0")
                        self.cells[i][i].config(state="disabled")
        self.n = new_n

    def fill_random(self):
        for i in range(0, self.n):
            for j in range(i, self.n):
                if i != j:
                    self.cells[i][j].delete(0, END)
                    r = randint(0, 1)
                    self.cells[i][j].insert(0, str(r))

    def clear(self):
        for i in range(self.n):
            for j in range(i, self.n):
                if i != j:
                    self.cells[i][j].delete(0, END)
