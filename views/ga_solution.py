from tkinter import BOTH, ttk

import networkx as nx
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from .config import SPRING_LAYOUT_SEED
from .solution_frame import SolutionFrame


class GASolution(ttk.Frame):
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
        self.convergence_tab = ttk.Frame(tabs)
        tabs.add(solution_tab, text="Solution")
        tabs.add(self.convergence_tab, text="Convergence")
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
        self.draw_convergence()

    def draw_convergence(self):
        fig = Figure(figsize=(7.5, 6), dpi=100)
        x = np.arange(0, self.coloring.max_generations + 1)
        ax = fig.add_subplot(111)
        avgs_fitness = self.results["execution_info"][0]
        ax.plot(x, avgs_fitness)
        ax.set_title(self.coloring.g.name, fontsize=13 or "Custom")
        ax.set_xlabel("Génération")
        ax.set_ylabel("Fitness moyenne")
        canvas = FigureCanvasTkAgg(fig, master=self.convergence_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.convergence_tab)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
