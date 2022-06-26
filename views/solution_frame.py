from tkinter import BOTH, ttk

import networkx as nx
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from .config import SPRING_LAYOUT_SEED, BASE_PADDING


class SolutionFrame(ttk.Frame):
    def __init__(self, master, technique_name, coloring, t, parameters=None):
        super().__init__(master)
        self.technique_name = technique_name
        self.coloring = coloring
        self.t = t
        self.parameters = parameters
        self.draw_graph()

    def draw_graph(self):
        graph = nx.from_numpy_array(np.array(self.coloring.adj_mat))
        graph_pos = nx.spring_layout(graph, seed=SPRING_LAYOUT_SEED)
        fig = Figure(figsize=(7.5, 6), dpi=100)
        instance = self.coloring.g
        fig.suptitle(
            f"{instance.name or 'Custom'}, V={instance.v}, E={instance.e}",
            fontweight="bold",
        )
        ax = fig.add_subplot(111)
        solution_info = (
            f"{self.technique_name} k ={self.coloring.solution[0]}, t={self.t:0.4f}s"
        )
        if self.parameters:
            parameters_values = ", ".join(
                [
                    f"{alias}={getattr(self.coloring, parameter)}"
                    for parameter, alias in self.parameters.items()
                ]
            )
            ax_title = f"{solution_info}\n{parameters_values}"
        else:
            ax_title = f"{solution_info}"
        ax.set_title(ax_title, fontsize=13)
        v = self.coloring.g.v
        colors_map = {}
        node_colors = [None] * v
        for i in range(v):
            virtual_color = self.coloring.solution[1][i]
            if virtual_color not in colors_map:
                colors_map[virtual_color] = np.random.rand(3)
            node_colors[i] = colors_map[virtual_color]
        nx.draw(graph, graph_pos, ax=ax, node_color=node_colors, node_size=400)
        if v <= 81:
            nx.draw_networkx_labels(
                graph,
                graph_pos,
                {i: i + 1 for i in range(v)},
                font_weight="bold",
                ax=ax,
            )
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
