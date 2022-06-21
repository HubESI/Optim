from tkinter import ttk

from .adjacency_matrix import ConfigurableAdjacencyMatrix
from .config import base_padding, n_max
from .instance_choice import InstanceChoice


class GenericTechniqueView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.conf_adj_matrix = ConfigurableAdjacencyMatrix(self, n_max)
        self.conf_adj_matrix.grid(
            row=0, column=0, rowspan=2, padx=base_padding, pady=base_padding
        )
        instance_choice0 = InstanceChoice(self)
        instance_choice0.grid(row=0, column=1, padx=base_padding, pady=base_padding)
        self.instance_choice = InstanceChoice(self)
        self.instance_choice.grid(row=1, column=1, padx=base_padding, pady=base_padding)
        solve_btn = ttk.Button(self, text="Exécuter", command=lambda: print("solve"))
        solve_btn.grid(row=2, column=1, padx=base_padding, pady=base_padding)
