import multiprocessing
import threading
from tkinter import messagebox, ttk

from opt_techniques.graph import Graph

from .adjacency_matrix import ConfigurableAdjacencyMatrix
from .config import BASE_PADDING, BOLD_FONT, N_MAX
from .instance_choice import InstanceChoice


class GenericTechniqueView(ttk.Frame):
    def __init__(self, master, coloring_class, parameters_class=None):
        super().__init__(master)
        self.coloring_class = coloring_class
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
            self.parameters = parameters_class(self)
            self.parameters.grid(
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

        def on_adj_matrix_select():
            self.conf_adj_matrix.enable()
            self.info_label["text"] = ""

        def on_file_select():
            self.conf_adj_matrix.disable()

        def on_successful_loading():
            self.info_label["text"] = ""

        self.instance_choice = InstanceChoice(
            self, on_adj_matrix_select, on_file_select, on_successful_loading
        )
        self.instance_choice.grid(
            row=row_count, column=1, padx=BASE_PADDING, pady=BASE_PADDING
        )
        row_count += 1
        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=row_count, column=1, padx=BASE_PADDING, sticky="we")
        row_count += 1
        self.solve_btn = ttk.Button(self, text="Exécuter", command=self.solve)
        self.solve_btn.grid(
            row=row_count, column=1, padx=BASE_PADDING, pady=BASE_PADDING
        )
        row_count += 1
        self.info_label = ttk.Label(self)
        self.info_label.grid(
            row=row_count, column=1, padx=BASE_PADDING, pady=BASE_PADDING
        )
        row_count += 1
        self.conf_adj_matrix.grid(
            row=1, column=0, rowspan=row_count - 1, padx=BASE_PADDING, pady=BASE_PADDING
        )

    def solve(self):
        if self.instance_choice.is_file_selected():
            instance = self.instance_choice.get_file_instance()
            if instance is None:
                self.info_label.config(foreground="red")
                self.info_label[
                    "text"
                ] = "Veuillez sélectionner un fichier d'une instance"
                return
        else:
            instance = Graph(self.conf_adj_matrix.get_matrix())
        coloring = self.coloring_class(instance, **self.parameters.get_kwargs())

        def solve_thread_job():
            def solve_process_job(results):
                r = coloring.solve()
                results.extend(r)

            results = multiprocessing.Manager().list()
            solve_process = multiprocessing.Process(
                target=solve_process_job, args=(results,), daemon=True
            )
            info_message = "L'exécution est terminée"

            def kill_solve_process():
                nonlocal info_message
                solve_process.kill()
                info_message = "L'exécution a été arrêtée"

            solve_process.start()
            self.solve_btn.config(text="Arrêter", command=kill_solve_process)
            solve_process.join()
            messagebox.showinfo(parent=self, title="Notification", message=info_message)
            print(results)
            self.info_label.config(text="")
            self.solve_btn.config(text="Exécuter", command=self.solve)

        threading.Thread(target=solve_thread_job, daemon=True).start()
        self.info_label.config(foreground="blue")
        self.info_label.config(
            text="L'algorithme est en cours d'exécution\nVous serez averti quand il se termine"
        )
