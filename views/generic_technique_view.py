import multiprocessing
import threading
from tkinter import HORIZONTAL, LEFT, X, messagebox, ttk

from opt_techniques.graph import Graph

from .adjacency_matrix import ConfigurableAdjacencyMatrix
from .config import BASE_PADDING, BOLD_FONT, N_MAX
from .instance_choice import InstanceChoice


class GenericTechniqueView(ttk.Frame):
    def __init__(self, master, coloring_class, parameters_class=None):
        super().__init__(master)
        self.coloring_class = coloring_class
        adj_matrix_frame = ttk.Frame(self)
        adj_matrix_frame.pack(side=LEFT, padx=BASE_PADDING, pady=BASE_PADDING)
        adj_matrix_label = ttk.Label(
            adj_matrix_frame, text="Matrice d'adjacence", font=BOLD_FONT
        )
        adj_matrix_label.pack(padx=BASE_PADDING)
        self.conf_adj_matrix = ConfigurableAdjacencyMatrix(adj_matrix_frame, N_MAX)
        self.conf_adj_matrix.pack(padx=BASE_PADDING)
        tweaks_frame = ttk.Frame(self)
        tweaks_frame.pack(side=LEFT, padx=BASE_PADDING, pady=BASE_PADDING)
        instance_choice_frame = ttk.Frame(tweaks_frame)
        instance_choice_frame.pack(pady=BASE_PADDING)
        instance_choice_label = ttk.Label(
            instance_choice_frame, text="Source de l'instance", font=BOLD_FONT
        )
        instance_choice_label.pack(pady=BASE_PADDING)

        def on_adj_matrix_select():
            self.conf_adj_matrix.enable()
            self.info_label.config(text="")

        def on_file_select():
            self.conf_adj_matrix.disable()

        def on_successful_loading():
            self.info_label.config(text="")

        self.instance_choice = InstanceChoice(
            instance_choice_frame,
            on_adj_matrix_select,
            on_file_select,
            on_successful_loading,
        )
        self.instance_choice.pack(pady=BASE_PADDING)
        separator = ttk.Separator(tweaks_frame, orient=HORIZONTAL)
        separator.pack(fill=X, expand=1, pady=BASE_PADDING)
        if parameters_class:
            technique_parameters_frame = ttk.Frame(tweaks_frame)
            technique_parameters_frame.pack(pady=BASE_PADDING)
            technique_parameters_label = ttk.Label(
                technique_parameters_frame,
                text="Paramètres de la méthode",
                font=BOLD_FONT,
            )
            technique_parameters_label.pack(pady=BASE_PADDING)
            self.parameters = parameters_class(technique_parameters_frame)
            self.parameters.pack(pady=BASE_PADDING)
            separator = ttk.Separator(tweaks_frame, orient=HORIZONTAL)
            separator.pack(fill=X, expand=1, pady=BASE_PADDING)
        solve_frame = ttk.Frame(tweaks_frame)
        solve_frame.pack(pady=BASE_PADDING)
        self.solve_btn = ttk.Button(solve_frame, text="Exécuter", command=self.solve)
        self.solve_btn.pack(pady=BASE_PADDING)
        self.info_label = ttk.Label(solve_frame)
        self.info_label.pack(pady=BASE_PADDING)

    def solve(self):
        print(self.master.winfo_width(), self.master.winfo_height())
        if self.instance_choice.is_file_selected():
            instance = self.instance_choice.get_file_instance()
            if instance is None:
                self.info_label.config(foreground="red")
                self.info_label.config(
                    text="Veuillez sélectionner un fichier d'une instance"
                )
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
            self.parameters.disable()
            self.instance_choice.disable()
            self.solve_btn.config(text="Arrêter", command=kill_solve_process)
            solve_process.join()
            messagebox.showinfo(parent=self, title="Notification", message=info_message)
            self.info_label.config(text="")
            self.solve_btn.config(text="Exécuter", command=self.solve)
            # open solutoin window
            t = results[1]
            print(t, coloring.solution)
            # after that
            self.parameters.enable()
            self.instance_choice.enable()

        threading.Thread(target=solve_thread_job, daemon=True).start()
        self.info_label.config(foreground="blue")
        self.info_label.config(
            text="L'algorithme est en cours d'exécution\nVous serez averti quand il se termine"
        )
