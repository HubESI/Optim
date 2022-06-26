from tkinter import BOTH, ttk

import networkx as nx
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from .config import SPRING_LAYOUT_SEED
from .solution_frame import SolutionFrame


class VDWOASolution(ttk.Frame):
    def __init__(
        self,
        master,
        technique_name,
        coloring,
        results,
        parameters=None,
        parameters_values_aliases=None,
    ):
        super().__init__(master)
        self.technique_name = technique_name
        self.coloring = coloring
        self.results = results
        self.parameters = parameters
        self.parameters_values_aliases = parameters_values_aliases
        tabs = ttk.Notebook(self)
        solution_tab = ttk.Frame(tabs)
        self.fitness_tab = ttk.Frame(tabs)
        self.conflicts_tab = ttk.Frame(tabs)
        tabs.add(solution_tab, text="Solution")
        tabs.add(self.fitness_tab, text="Fitness")
        tabs.add(self.conflicts_tab, text="Conflits")
        tabs.pack(fill=BOTH, expand=1)
        base_solution_frame = SolutionFrame(
            solution_tab,
            technique_name,
            coloring,
            results,
            parameters,
            parameters_values_aliases,
        )
        base_solution_frame.pack(fill=BOTH, expand=1)
        self.draw_fitness_convergence()
        self.draw_conflicts_convergence()

    def draw_fitness_convergence(self):
        execution_info = self.results["execution_info"]
        fig = Figure(figsize=(7.5, 6), dpi=100)
        nb_iter = execution_info[0][0]
        x = np.arange(0, nb_iter)
        ax = fig.add_subplot(111)
        fitness_per_iter = execution_info[0][1]
        ax.plot(x, fitness_per_iter[:nb_iter])
        ax.set_title(self.coloring.g.name or "Custom", fontsize=13)
        ax.set_xlabel("Itération", fontsize=12)
        ax.set_ylabel("Fitness du meilleur agent", fontsize=12)
        canvas = FigureCanvasTkAgg(fig, master=self.fitness_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.fitness_tab)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)

    def draw_conflicts_convergence(self):
        execution_info = self.results["execution_info"]
        fig = Figure(figsize=(7.5, 6), dpi=100)
        nb_iter = execution_info[0][0]
        x = np.arange(0, nb_iter)
        ax = fig.add_subplot(111)
        conflicts_per_iter = execution_info[0][2]
        ax.plot(x, conflicts_per_iter[:nb_iter])
        ax.set_title(self.coloring.g.name or "Custom", fontsize=13)
        ax.set_xlabel("Itération", fontsize=12)
        ax.set_ylabel("Nombre de conflits", fontsize=12)
        canvas = FigureCanvasTkAgg(fig, master=self.conflicts_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.conflicts_tab)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
