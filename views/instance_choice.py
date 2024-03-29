import textwrap
from tkinter import BooleanVar, filedialog, ttk

from opt_techniques.graph import Graph

from .config import BASE_PADDING


class InstanceChoice(ttk.Frame):
    info_label_width = 40
    radiobtn_width = 20
    btn_width = 10

    def __init__(
        self,
        master,
        save_adj_matrix,
        on_adj_matrix_select,
        on_file_select,
        on_successful_loading,
    ):
        super().__init__(master)
        self.file_instance = None
        self.choice = BooleanVar(self, False)
        self.on_successful_loading = on_successful_loading

        def on_adj_matrix_select_wrapper():
            on_adj_matrix_select()
            self.file_instance = None
            self.info_label.config(text="")
            self.import_btn.config(state="disabled")
            self.save_btn.config(state="normal")

        def on_file_select_wrapper():
            on_file_select()
            self.info_label.config(text="")
            self.import_btn.config(state="normal")
            self.save_btn.config(state="disabled")

        def save_adj_matrix_wrapper():
            if save_adj_matrix():
                self.info_label.config(foreground="blue")
                self.info_label.config(text="Instance sauvegardée avec succés")
            else:
                self.info_label.config(foreground="red")
                self.info_label.config(text="Échec de la sauvegarde")

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
        self.save_btn = ttk.Button(
            self,
            text="Sauvegarder",
            width=self.btn_width,
            command=save_adj_matrix_wrapper,
        )
        self.save_btn.grid(row=0, column=1, padx=BASE_PADDING, pady=BASE_PADDING)
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
            self,
            text="Importer",
            width=self.btn_width,
            state="disabled",
            command=self.import_file,
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
        if not filename:
            return
        try:
            self.file_instance = Graph.from_file(filename)
            instance_name = filename.split("/")[-1]
            self.info_label.config(foreground="blue")
            info_str = (
                f'Instance chargée avec succès depuis le fichier "{instance_name}"'
            )
            info_str = "\n".join(textwrap.wrap(info_str, width=self.info_label_width))
            self.info_label.config(text=info_str)
            self.on_successful_loading()
        except Exception as e:
            print(e)
            self.file_instance = None
            self.info_label.config(foreground="red")
            self.info_label.config(text="Le fichier sélectionné est invalide")

    def disable(self):
        self.adj_matrix_choice.config(state="disabled")
        self.file_choice.config(state="disabled")
        self.import_btn.config(state="disabled")

    def enable(self):
        self.adj_matrix_choice.config(state="normal")
        self.file_choice.config(state="normal")
        if self.is_file_selected():
            self.import_btn.config(state="normal")
