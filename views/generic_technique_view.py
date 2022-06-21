from tkinter import ttk

from .adjacency_matrix import ConfigurableAdjacencyMatrix
from .config import base_padding, bold_font, n_max
from .instance_choice import InstanceChoice


class GenericTechniqueView(ttk.Frame):
    def __init__(self, master, parameters_frame=0):
        super().__init__(master)
        adj_matrix_label = ttk.Label(self, text="Matrice d'adjacence", font=bold_font)
        adj_matrix_label.grid(row=0, column=0, padx=base_padding, pady=base_padding)
        self.conf_adj_matrix = ConfigurableAdjacencyMatrix(self, n_max)
        row_count = 1
        if parameters_frame:
            technique_parameters_label = ttk.Label(
                self, text="Paramètres de la méthode", font=bold_font
            )
            technique_parameters_label.grid(
                row=row_count, column=1, padx=base_padding, pady=base_padding
            )
            row_count += 1
            instance_choice0 = InstanceChoice(self)
            instance_choice0.grid(
                row=row_count, column=1, padx=base_padding, pady=base_padding
            )
            row_count += 1
            separator = ttk.Separator(self, orient="horizontal")
            separator.grid(row=row_count, column=1, padx=base_padding, sticky="we")
            row_count += 1
        instance_choice_label = ttk.Label(
            self, text="Source de l'instance", font=bold_font
        )
        instance_choice_label.grid(
            row=row_count, column=1, padx=base_padding, pady=base_padding
        )
        row_count += 1
        self.instance_choice = InstanceChoice(self)
        self.instance_choice.grid(
            row=row_count, column=1, padx=base_padding, pady=base_padding
        )
        row_count += 1
        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=row_count, column=1, padx=base_padding, sticky="we")
        row_count += 1
        solve_btn = ttk.Button(self, text="Exécuter", command=lambda: print("solve"))
        solve_btn.grid(row=row_count, column=1, padx=base_padding, pady=base_padding)
        row_count += 1
        self.info_label = ttk.Label(self)
        self.info_label.grid(
            row=row_count, column=1, padx=base_padding, pady=base_padding
        )
        row_count += 1
        print(row_count)
        self.conf_adj_matrix.grid(
            row=1, column=0, rowspan=row_count - 1, padx=base_padding, pady=base_padding
        )
