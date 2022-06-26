import multiprocessing
import threading
from tkinter import BOTH, HORIZONTAL, LEFT, Toplevel, X, messagebox, ttk
from tkinter.filedialog import asksaveasfile

import networkx as nx
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from opt_techniques.graph import Graph

from .adjacency_matrix import ConfigurableAdjacencyMatrix
from .config import BASE_PADDING, BOLD_FONT, N_MAX, SPRING_LAYOUT_SEED
from .instance_choice import InstanceChoice
from .solution_frame import SolutionFrame


class GenericTechniqueView(ttk.Frame):
    def __init__(self, master, technique_name, coloring_class, parameters_class=None):
        super().__init__(master)
        self.technique_name = technique_name
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
            self.preview_btn.config(state="normal")

        def on_file_select():
            self.conf_adj_matrix.disable()
            self.preview_btn.config(state="disabled")

        def on_successful_loading():
            self.info_label.config(text="")
            self.preview_btn.config(state="normal")

        self.instance_choice = InstanceChoice(
            instance_choice_frame,
            self.save_adj_matrix,
            on_adj_matrix_select,
            on_file_select,
            on_successful_loading,
        )
        self.instance_choice.pack(pady=BASE_PADDING)
        self.preview_btn = ttk.Button(
            tweaks_frame,
            text="Visualiser",
            command=self.preview_graph,
        )
        self.preview_btn.pack(pady=BASE_PADDING)
        separator = ttk.Separator(tweaks_frame, orient=HORIZONTAL)
        separator.pack(fill=X, expand=1, pady=BASE_PADDING)
        self.parameters = None
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

    def preview_graph(self):
        self.preview_btn.config(state="disabled")
        preview = Toplevel(self)

        def on_closing():
            self.preview_btn.config(state="normal")
            preview.destroy()

        preview.protocol("WM_DELETE_WINDOW", on_closing)
        instance = self.get_instance()
        preview.title(f"Visualisation du graphe {instance.name or 'Custom'}")
        adj_mat = np.array(instance.adj_mat)
        graph = nx.from_numpy_array(adj_mat)
        graph_pos = nx.spring_layout(graph, seed=SPRING_LAYOUT_SEED)

        def draw_graph():
            fig = Figure(figsize=(6, 5), dpi=100)
            fig.suptitle(
                f"{instance.name or 'Custom'}, V={instance.v}, E={instance.e}",
                fontweight="bold",
            )
            ax = fig.add_subplot(111)
            nx.draw(
                graph,
                graph_pos,
                ax=ax,
                node_size=400,
                node_color="white",
                edgecolors="black",
            )
            if len(adj_mat) <= 81:
                nx.draw_networkx_labels(
                    graph,
                    graph_pos,
                    {i: i + 1 for i in range(len(adj_mat))},
                    font_weight="bold",
                    ax=ax,
                )
            canvas = FigureCanvasTkAgg(fig, master=preview)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=1)
            toolbar = NavigationToolbar2Tk(canvas, preview)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        draw_graph()

    def save_adj_matrix(self):
        f = asksaveasfile(
            parent=self,
            filetypes=[("DIMACS", "*.col"), ("Other", "*")],
            defaultextension=".col",
            initialfile="custom",
        )
        if not f:
            return False
        try:
            Graph(self.conf_adj_matrix.get_matrix()).to_file(f.name)
            return True
        except Exception as e:
            print(e)
            return False

    def get_instance(self):
        if self.instance_choice.is_file_selected():
            return self.instance_choice.get_file_instance()
        else:
            return Graph(self.conf_adj_matrix.get_matrix())

    def solve(self):
        instance = self.get_instance()
        if instance is None:
            self.info_label.config(foreground="red")
            self.info_label.config(
                text="Veuillez sélectionner un fichier d'une instance"
            )
            return
        if self.parameters is None:
            coloring = self.coloring_class(instance)
        else:
            coloring = self.coloring_class(instance, **self.parameters.get_kwargs())

        def solve_thread_job(thread_results):
            def solve_process_job(coloring, attrs_needed, process_results):
                r = coloring.solve()
                for attr in attrs_needed:
                    process_results[attr] = getattr(coloring, attr)
                process_results["time"] = r[1]

            process_results = multiprocessing.Manager().dict()
            attrs_needed = ["solution"]
            solve_process = multiprocessing.Process(
                target=solve_process_job,
                args=(coloring, attrs_needed, process_results),
                daemon=True,
            )
            killed = False

            def kill_solve_process():
                nonlocal killed
                solve_process.kill()
                killed = True

            solve_process.start()
            if self.parameters:
                self.parameters.disable()
            self.instance_choice.disable()
            self.solve_btn.config(text="Arrêter", command=kill_solve_process)
            solve_process.join()
            if killed:
                info_message = "L'exécution a été arrêtée"
            else:
                info_message = "L'exécution est terminée"
            messagebox.showinfo(parent=self, title="Notification", message=info_message)
            self.info_label.config(text="")
            self.solve_btn.config(text="Exécuter", command=self.solve)
            if self.parameters:
                self.parameters.enable()
            self.instance_choice.enable()
            if not killed:
                # open solutoin window
                coloring.solution = process_results["solution"]
                for r in process_results:
                    thread_results[r] = process_results[r]
                self.event_generate("<<EXECUTION_DONE>>", when="tail")

        def open_solution_window(e):
            t = thread_results["time"]
            solution_window = Toplevel(self)
            solution_window.title(
                f"{instance.name or 'Custom'} avec {self.technique_name}"
            )
            if self.parameters is None:
                solution_frame = SolutionFrame(
                    solution_window,
                    self.technique_name,
                    coloring,
                    t,
                )
            else:
                solution_frame = SolutionFrame(
                    solution_window,
                    self.technique_name,
                    coloring,
                    t,
                    self.parameters.get_aliases(),
                )
            solution_frame.pack(fill=BOTH, expand=1)

        thread_results = {}
        self.bind("<<EXECUTION_DONE>>", open_solution_window)
        threading.Thread(
            target=solve_thread_job, args=(thread_results,), daemon=True
        ).start()
        self.info_label.config(foreground="blue")
        self.info_label.config(
            text="L'algorithme est en cours d'exécution\nVous serez averti quand il se termine"
        )
