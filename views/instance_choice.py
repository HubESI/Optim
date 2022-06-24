import textwrap
from tkinter import BooleanVar, filedialog, ttk

from opt_techniques.graph import Graph

from .config import BASE_PADDING


class InstanceChoice(ttk.Frame):
    info_label_width = 40
    radiobtn_width = 20

    def __init__(
        self, master, on_adj_matrix_select, on_file_select, on_successful_loading
    ):
        super().__init__(master)
        self.file_instance = None
        self.choice = BooleanVar(self, False)
        self.on_successful_loading = on_successful_loading

        def on_adj_matrix_select_wrapper():
            on_adj_matrix_select()
            self.file_instance = None
            self.info_label["text"] = ""
            self.import_btn.config(state="disabled")

        def on_file_select_wrapper():
            on_file_select()
            self.import_btn.config(state="normal")

        self.adj_matrix_choice = ttk.Radiobutton(
            self,
            text="Matrice entrée",
            variable=self.choice,
            value=False,
            command=on_adj_matrix_select_wrapper,
            width=self.radiobtn_width,
        )
        self.adj_matrix_choice.grid(
            row=0, column=0, padx=BASE_PADDING, pady=BASE_PADDING
        )
        self.file_choice = ttk.Radiobutton(
            self,
            text="Fichier (format DIMACS)",
            variable=self.choice,
            value=True,
            command=on_file_select_wrapper,
            width=self.radiobtn_width,
        )
        self.file_choice.grid(row=1, column=0, padx=BASE_PADDING, pady=BASE_PADDING)
        self.import_btn = ttk.Button(
            self, text="Importer", state="disabled", command=self.import_file
        )
        self.import_btn.grid(row=1, column=1, padx=BASE_PADDING, pady=BASE_PADDING)
        self.info_label = ttk.Label(self, width=self.info_label_width)
        self.info_label.grid(
            row=2, column=0, columnspan=2, padx=BASE_PADDING, pady=BASE_PADDING
        )

    def is_file_selected(self):
        return self.choice.get()

    def is_adj_matrix_selected(self):
        return not self.is_file_selected()

    def get_file_instance(self):
        return self.file_instance

    def import_file(self):
        filename = filedialog.askopenfilename(
            parent=self,
            filetypes=[("DIMACS", "*.col"), ("Other", "*")],
            title="Veuillez choisir le fichier de l'instance",
        )
        try:
            self.file_instance = Graph.from_file(filename)
            instance_name = filename.split("/")[-1]
            self.info_label.config(foreground="blue")
            info_str = (
                f'Instance chargée avec succès depuis le fichier "{instance_name}"'
            )
            info_str = "\n".join(textwrap.wrap(info_str, width=self.info_label_width))
            self.info_label["text"] = info_str
            self.on_successful_loading()
        except Exception:
            self.file_instance = None
            self.info_label.config(foreground="red")
            self.info_label["text"] = "Le fichier sélectionné est invalide"

    def disable(self):
        self.adj_matrix_choice.config(state="disabled")
        self.file_choice.config(state="disabled")
        self.import_btn.config(state="disabled")

    def enable(self):
        self.adj_matrix_choice.config(state="normal")
        self.file_choice.config(state="normal")
        self.import_btn.config(state="normal")