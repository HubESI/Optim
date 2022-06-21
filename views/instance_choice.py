from random import randint
from tkinter import CENTER, END, ttk, BooleanVar, filedialog

from .config import base_padding, bold_font
from opt_techniques.graph import Graph


class InstanceChoice(ttk.Frame):
    radiobtn_width = 20

    def __init__(self, master):
        super().__init__(master)
        self.file_instance = None
        instance_choice_label = ttk.Label(
            self, text="Source de l'instance", font=bold_font
        )
        instance_choice_label.grid(
            row=0, column=0, padx=base_padding, pady=base_padding
        )
        self.choice = BooleanVar(self, False)
        adj_matrix_choice = ttk.Radiobutton(
            self,
            text="Matrice entrée",
            variable=self.choice,
            value=False,
            command=lambda: self._on_adj_matrix_select(),
            width=self.radiobtn_width,
        )
        adj_matrix_choice.grid(row=1, column=0, padx=base_padding, pady=base_padding)
        file_choice = ttk.Radiobutton(
            self,
            text="Fichier (format DIMACS)",
            variable=self.choice,
            value=True,
            command=lambda: self._on_file_select(),
            width=self.radiobtn_width,
        )
        file_choice.grid(row=2, column=0, padx=base_padding, pady=base_padding)
        self.import_btn = ttk.Button(
            self, text="Importer", state="disabled", command=lambda: self.import_file()
        )
        self.import_btn.grid(row=2, column=1, padx=base_padding, pady=base_padding)
        self.info_label = ttk.Label(self)
        self.info_label.grid(row=3, column=0, padx=base_padding, pady=base_padding)

    def _on_adj_matrix_select(self):
        self.file_instance = None
        self.info_label["text"] = ""
        self.import_btn.config(state="disabled")

    def _on_file_select(self):
        self.import_btn.config(state="normal")

    def is_file_selected(self):
        return self.choice

    def is_adj_matrix_selected(self):
        return not self.choice

    def get_file_instance(self):
        return self.file_instance()

    def import_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("DIMACS", "*.col"), ("Other", "*")],
            title="Veuillez choisir le fichier de l'instance",
        )
        try:
            self.file_instance = Graph.from_file(filename)
            instance_name = filename.split("/")[-1]
            self.info_label.config(foreground="black")
            self.info_label[
                "text"
            ] = f'Instance chargée avec succès depuis le fichier "{instance_name}"'
        except Exception:
            self.file_instance = None
            self.info_label.config(foreground="red")
            self.info_label["text"] = "Le fichier sélectionné est invalide"
