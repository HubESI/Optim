from tkinter import ttk

from .adjacency_matrix import ConfigurableAdjacencyMatrix
from .config import base_padding, bold_font, n_max
from .instance_choice import InstanceChoice


class GenericTechniqueView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        adj_matrix_label = ttk.Label(self, text="Matrice d'adjacence", font=bold_font)
        adj_matrix_label.grid(row=0, column=0, padx=base_padding, pady=base_padding)
        self.conf_adj_matrix = ConfigurableAdjacencyMatrix(self, n_max)
        self.conf_adj_matrix.grid(
            row=1, column=0, rowspan=5, padx=base_padding, pady=base_padding
        )
        technique_parameters_label = ttk.Label(
            self, text="Paramètres de la méthode", font=bold_font
        )
        technique_parameters_label.grid(
            row=1, column=1, padx=base_padding, pady=base_padding
        )
        instance_choice0 = InstanceChoice(self)
        instance_choice0.grid(row=2, column=1, padx=base_padding, pady=base_padding)
        instance_choice_label = ttk.Label(
            self, text="Source de l'instance", font=bold_font
        )
        instance_choice_label.grid(
            row=3, column=1, padx=base_padding, pady=base_padding
        )
        self.instance_choice = InstanceChoice(self)
        self.instance_choice.grid(row=4, column=1, padx=base_padding, pady=base_padding)
        solve_btn = ttk.Button(self, text="Exécuter", command=lambda: print("solve"))
        solve_btn.grid(row=5, column=1, padx=base_padding, pady=base_padding)
