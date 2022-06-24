from tkinter import ttk

from .adjacency_matrix import ConfigurableAdjacencyMatrix
from .config import BASE_PADDING, BOLD_FONT, N_MAX
from .instance_choice import InstanceChoice


class GenericTechniqueView(ttk.Frame):
    def __init__(self, master, parameters_class=None):
        super().__init__(master)
        adj_matrix_label = ttk.Label(self, text="Matrice d'adjacence", font=BOLD_FONT)
        adj_matrix_label.grid(row=0, column=0, padx=BASE_PADDING, pady=BASE_PADDING)
        self.conf_adj_matrix = ConfigurableAdjacencyMatrix(self, N_MAX)
        row_count = 1
        if parameters_class:
            technique_parameters_label = ttk.Label(
                self, text="Paramètres de la méthode", font=BOLD_FONT
            )
            technique_parameters_label.grid(
                row=row_count, column=1, padx=BASE_PADDING, pady=BASE_PADDING
            )
            row_count += 1
            parameters_frame = parameters_class(self)
            parameters_frame.grid(
                row=row_count, column=1, padx=BASE_PADDING, pady=BASE_PADDING
            )
            row_count += 1
            separator = ttk.Separator(self, orient="horizontal")
            separator.grid(row=row_count, column=1, padx=BASE_PADDING, sticky="we")
            row_count += 1
        instance_choice_label = ttk.Label(
            self, text="Source de l'instance", font=BOLD_FONT
        )
        instance_choice_label.grid(
            row=row_count, column=1, padx=BASE_PADDING, pady=BASE_PADDING
        )
        row_count += 1
        self.instance_choice = InstanceChoice(
            self, self.conf_adj_matrix.enable, self.conf_adj_matrix.disable
        )
        self.instance_choice.grid(
            row=row_count, column=1, padx=BASE_PADDING, pady=BASE_PADDING
        )
        row_count += 1
        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=row_count, column=1, padx=BASE_PADDING, sticky="we")
        row_count += 1
        solve_btn = ttk.Button(self, text="Exécuter", command=lambda: print("solve"))
        solve_btn.grid(row=row_count, column=1, padx=BASE_PADDING, pady=BASE_PADDING)
        row_count += 1
        self.info_label = ttk.Label(self)
        self.info_label.grid(
            row=row_count, column=1, padx=BASE_PADDING, pady=BASE_PADDING
        )
        row_count += 1
        self.conf_adj_matrix.grid(
            row=1, column=0, rowspan=row_count - 1, padx=BASE_PADDING, pady=BASE_PADDING
        )
